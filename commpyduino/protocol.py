#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mFoxRU'

from functools import reduce

from commpyduino.status_codes import Status


class CommProtocol:
    STX = 0x02
    ETX = 0x03
    ACK = 0x06
    NAK = 0x15
    ESC = 0x1B

    _ESCAPE_LIST = (
        (bytearray((ESC,)), bytearray((ESC, ESC))),
        (bytearray((STX,)), bytearray((ESC, STX))),
        (bytearray((ETX,)), bytearray((ESC, ETX))),
    )

    def __init__(self):
        self._frame_id = -1

    @property
    def frame_id(self) -> int:
        return self._frame_id

    def compose_request(self, cmd: int, data: bytearray=None) -> bytearray:
        if data is None:
            data = bytearray()
        # Increment frame id
        self._frame_id = (self.frame_id + 1) % 256
        # Calc frame length
        length = 6 + len(data)
        # Create request array
        request = bytearray((
            length // 256,
            length % 256,
            self.frame_id,
            cmd,
            *data
        ))
        # Calc CRC
        request.append(reduce(int.__xor__, request))
        # Escape characters
        for (from_, to) in self._ESCAPE_LIST:
            request = request.replace(from_, to)
        # Add STX and ETX
        request.insert(0, self.STX)
        request.append(self.ETX)

        return request

    def decompose_reply(self, msg: bytearray) -> dict:
        reply = {'raw': msg}
        # Remove STX and ETX
        msg: bytearray = msg[1:-1]
        # Unescape characters
        for (to, from_) in reversed(self._ESCAPE_LIST):
            msg = msg.replace(from_, to)
        # Check length
        print('Received: {}'.format(self.nicer(msg)))
        if len(msg) < 6:
            reply['status'] = Status.LEN_ERR
            return reply
        msg_length = msg[0]*256+msg[1]
        if msg_length != len(msg)+1:
            reply['status'] = Status.LEN_ERR
            return reply
        # Check CRC
        msg_crc = msg[-1]
        crc = reduce(int.__xor__, msg[:-1])
        if crc != msg_crc:
            reply['status'] = Status.CRC_ERR
            return reply
        # Extract data
        reply['frame_id'] = msg[2]
        if reply['frame_id'] != self.frame_id:
            reply['status'] = Status.ID_ERR
            return reply
        reply['status'] = Status(msg[3])
        reply['cmd'] = msg[4]
        reply['data'] = msg[5:-1]
        return reply

    @staticmethod
    def nicer(br) -> str:
        return ' '.join(str.zfill(hex(x)[2:], 2).upper() for x in br)
