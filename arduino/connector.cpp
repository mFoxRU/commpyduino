#include "connector.h"

void startConnector(unsigned long baudrate) {
    Serial.begin(baudrate);
}

void read_serial() {
    static bool escaping = false;
    static bool receiving = false;
    static uint8_t curr_byte = 0x00;
    
    while (Serial.available()) {
        curr_byte = Serial.read();
        // Check if received escape byte in non-escaping mode
        if (!escaping && curr_byte == ESC) { // 1
            escaping = true;
            continue;
        }
        // Seems like it's a message start
        if (!escaping && curr_byte == STX) { // 2
            receiving = true;
            msg_len = 0;
        }
        // Seems like it's a message end
        else if (receiving && !escaping && curr_byte == ETX) { // 3
            receiving = false;
            // Check if message was properly received
            if (request_valid())
                Serial.write(ACK);
            else {
                Serial.write(NAK);
                return;
            }
            
            // Execute command and place reply in msg
            execute_command();
            
            // Set length
            msg[0] = (uint8_t) (msg_len+1 >> 8);
            msg[1] = (uint8_t) (msg_len+1 & 255);
            
            // Calculate CRC
            msg[msg_len-1] = msg[0];
            for (uint16_t x=1; x<msg_len-1; x++)
                msg[msg_len-1] ^= msg[x];
                
            // Send reply and wait for ACK
            for (uint8_t x=0; x<3; x++) {
                Serial.write(STX);
                for (uint16_t b=0; b<msg_len; b++) {
                    if (msg[b] == STX || msg[b] == ETX || msg[b] == ESC)
                        Serial.write(ESC);
                    Serial.write(msg[b]);
                }
                Serial.write(ETX);
                delay(SEND_TIMEOUT);
                uint8_t reply = Serial.read();
                if (reply == ACK)
                    break;
            }
            if (planning_reset) {
                planning_reset = false;
                Commands::soft_reset();
            }
                
            return;
        }
        // Seems like it's a new message byte
        else if (receiving) { // 4
            msg[msg_len] = curr_byte;
            msg_len += 1;
        }
        if (escaping)
            escaping = false;
    }
}

bool request_valid() {
    // Check length
    uint16_t msg_extracted_len = (uint16_t) msg[0] << 8 | msg[1];
    if (msg_len+1 != msg_extracted_len)
        return false;
    // Check CRC
    uint8_t CRC = 0;
    for (uint16_t i=0; i<msg_len-1; i++)
        CRC ^= msg[i];  
    if (CRC != msg[msg_len-1])
        return false;
    // Message OK
    
    return true;
}

void execute_command() {
    uint8_t curr_command = msg[3];
    // Below, msg_len will be counted without ETX
    switch (curr_command) {
        case 0x21:  // Soft reset
            msg_len = 6;
            msg[3] = 0x00;
            planning_reset = true;
            break;
        case 0x22:  // Get buffer size
            msg_len = 8;
            msg[3] = 0x00;
            msg[5] = (uint8_t) (Commands::get_buffer_size() >> 8);
            msg[6] = (uint8_t) (Commands::get_buffer_size() & 255);
            break;
        case 0x31:  // Set pin mode
            msg_len = 6;
            msg[3] = 0x00;
            Commands::set_pin_mode(msg[4], msg[5]);
            break;
        case 0x40:  // Digital read
            msg_len = 7;
            msg[3] = 0x00;
            msg[5] = (uint8_t) Commands::digital_read(msg[4]);
            break;
        case 0x41:  // Digital write
            msg_len = 6;
            msg[3] = 0x00;
            Commands::digital_write(msg[4], (bool) msg[5]);
            break;
        case 0x42:  // Digital write timeout
            msg_len = 6;
            msg[3] = 0x00;
            Commands::digital_write_timeout(msg[4], (bool) msg[5], ((uint16_t) msg[6] << 8 | msg[7]));
            break;
        case 0x43:  // Digital write sequence
            msg_len = 6;
            msg[3] = 0x00;
            Commands::digital_write_sequence(msg[4], (bool) msg[5], msg[6], msg);
            break;
        case 0x50: { // Analog read
            msg_len = 8;
            msg[3] = 0x00;
            uint16_t value = Commands::analog_read(msg[4]);
            msg[5] = (uint8_t) (value >> 8);
            msg[6] = (uint8_t) (value & 255);
            break;
        }
        case 0x51:  // Analog write
            msg_len = 6;
            msg[3] = 0x00;
            Commands::analog_write(msg[4], msg[5]);
            break;   
    }      
    msg[4] = curr_command;
}






