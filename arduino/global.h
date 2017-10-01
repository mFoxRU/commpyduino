#ifndef GLOBAL_H
#define GLOBAL_H

// Default com baudrate (can also be changed when calling `startConnector()`)
#define DEFAULT_BAUDRATE 115200
// Buffer size. Modify depending on available memory. Do not set below 8
#define MSG_BUFFER_SIZE 256
// Delay between replying and reading ACK
#define SEND_TIMEOUT 300

#endif // GLOBAL_H
