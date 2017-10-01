#include "commands.h"

void Commands::soft_reset(){
    asm volatile ("  jmp 0");
}

uint16_t Commands::get_buffer_size(){
  return (uint16_t)MSG_BUFFER_SIZE;
}

void Commands::set_pin_mode(uint8_t pin, uint8_t mode) {
    pinMode(pin, mode);
}

bool Commands::digital_read(uint8_t pin) {
    return (bool) digitalRead(pin);
}

void Commands::digital_write(uint8_t pin, bool value){
    digitalWrite(pin, value);
}

void Commands::digital_write_timeout(uint8_t pin, bool value, uint16_t timeout) {
    digitalWrite(pin, value);
    delay((unsigned long) timeout);
    digitalWrite(pin, !value);
}

void Commands::digital_write_sequence(uint8_t pin, bool value, uint8_t N, uint8_t *timeouts) {
    for (uint16_t i=0; i<N*2; i+=2) {
        digitalWrite(pin, (i%4) ? !value : value);
        delay(timeouts[DWS_PADDING+i+1] | (unsigned long) timeouts[DWS_PADDING+i] << 8);
    }
    digitalWrite(pin, N%2 ? !value : value);
}

uint16_t Commands::analog_read(uint8_t pin){
    return analogRead(pin);
}

void Commands::analog_write(uint8_t pin, uint8_t value){
    analogWrite(pin, value);
}

