#ifndef COMMANDS_H
#define COMMANDS_H

#include "Arduino.h"
//#include <stdint.h>
#include "global.h"

#define DWS_PADDING 5

namespace Commands {
    void soft_reset();
    
    uint16_t get_buffer_size();
    
    void set_pin_mode(uint8_t pin, uint8_t mode);
    
    bool digital_read(uint8_t pin);
    void digital_write(uint8_t pin, bool value);
    void digital_write_timeout(uint8_t pin, bool value, uint16_t timeout);
    void digital_write_sequence(uint8_t pin, bool value, uint8_t N, uint8_t *timeouts);
    
    uint16_t analog_read(uint8_t pin);
    void analog_write(uint8_t pin, uint8_t value);
}

#endif // COMMANDS_H
