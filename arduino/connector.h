#ifndef CONNECTOR_H
#define CONNECTOR_H

#include "global.h"
#include "commands.h"

// Protocol constants
#define STX 0x02
#define ETX 0x03
#define ACK 0x06
#define NAK 0x15
#define ESC 0x1B

static uint8_t msg[MSG_BUFFER_SIZE];
static uint16_t msg_len = 0;
static bool planning_reset = false;


void startConnector(unsigned long baudrate=DEFAULT_BAUDRATE);
void read_serial();
bool request_valid();
void execute_command();

#endif // CONNECTOR_H
