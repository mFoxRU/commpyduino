#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mFoxRU'

from typing import Iterable
from itertools import chain

from serial import Serial

from commpyduino.protocol import CommProtocol
from commpyduino.status_codes import Status


class Connector:

    def __init__(self, port: str, baudrate: int=115200):
        super().__init__()
        self._serial = Serial()
        self._serial.setPort(port)
        self._serial.baudrate = baudrate
        self._serial.timeout = .1

        self._protocol = CommProtocol()

        self._last_command = None
        self._last_reply = None

        self.commands = {
            'soft_reset': self.soft_reset,
            'get_buffer_size': self.get_buffer_size,
            'set_pin_mode': self.set_pin_mode,
            'digital_read': self.digital_read,
            'digital_write': self.digital_write,
            'digital_write_timeout': self.digital_write_timeout,
            'digital_write_sequence': self.digital_write_sequence,
            'analog_read': self.analog_read,
            'analog_write': self.analog_write,
        }

    def _communicate(self, cmd: int, data: bytearray=None) -> dict:
        self._last_command = cmd
        message = self._protocol.compose_request(cmd, data)
        if not self._serial.isOpen():
            try:
                self._serial.open()
            except Exception as e:
                self._last_reply = {'status': Status.REQ_ERR,
                                    'frame_id': self._protocol.frame_id}
                return self._last_reply

        self._serial.readall()
        # Send request
        for _try in range(3):
            self._serial.write(message)
            rep = self._serial.read(1)
            if rep[0] == self._protocol.ACK:
                break

            if _try == 2:
                self._last_reply = {'status': Status.NO_ACK,
                                    'frame_id': self._protocol.frame_id}
                return self._last_reply
        # Read reply
        for _try in range(3):
            while not self._serial.in_waiting:
                pass
            reply = self._serial.readall()
            self._last_reply = self._protocol.decompose_reply(bytearray(reply))
            # Check if reply is valid
            if self._last_reply['status'] not in (
                    Status.LEN_ERR, Status.CRC_ERR, Status.ID_ERR):
                # Seems legit
                self._serial.write(self._protocol.ACK)
                return self._last_reply

            # Seems not legit
            self._serial.write(self._protocol.NAK)

            # No more tries, deal with it
            if _try == 2:
                if 'frame_id' not in self._last_reply:
                    self._last_reply['frame_id'] = self._protocol.frame_id
                return self._last_reply

    @property
    def last_command(self) -> int:
        return self._last_command

    @property
    def last_reply(self) -> dict:
        return self._last_reply

    def soft_reset(self) -> dict:
        return self._communicate(0x21)

    def get_buffer_size(self) -> dict:
        reply = self._communicate(0x22)
        if 'data' in reply and len(reply['data']) == 2:
            reply['data'] = reply['data'][0] * 256 + reply['data'][1]
        return reply

    def set_pin_mode(self, pin: int, mode: int) -> dict:
        payload = bytearray((pin, mode))
        return self._communicate(0x31, payload)

    def digital_read(self, pin: int) -> dict:
        payload = bytearray((pin, ))
        reply = self._communicate(0x40, payload)
        if 'data' in reply and len(reply['data']) == 1:
            reply['data'] = reply['data'][0]
        return reply

    def digital_write(self, pin: int, value: int) -> dict:
        payload = bytearray((pin, value))
        return self._communicate(0x41, payload)

    def digital_write_timeout(self, pin: int, value: int, timeout: int) ->dict:
        payload = bytearray((pin, value, timeout // 256, timeout % 256))
        return self._communicate(0x42, payload)

    def digital_write_sequence(self, pin: int, value: int, n: int,
                               timeouts: Iterable) -> dict:
        payload = bytearray((pin, value, n))
        payload.extend(
            chain.from_iterable((x // 256, x % 256) for x in timeouts))
        return self._communicate(0x43, payload)

    def analog_read(self, pin: int) -> dict:
        payload = bytearray((pin, ))
        reply = self._communicate(0x50, payload)
        if 'data' in reply and len(reply['data']) == 2:
            reply['data'] = reply['data'][0] * 256 + reply['data'][1]
        return reply

    def analog_write(self, pin: int, value: int) -> dict:
        payload = bytearray((pin, value))
        return self._communicate(0x51, payload)
