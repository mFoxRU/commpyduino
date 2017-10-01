#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mFoxRU'


class _StatusCodes:
    inst = {}

    _desc = {
        0x00: 'OK',
        0x01: 'Could not send request',
        0x02: 'Didn\'t receive ACK',
        0x03: 'Didn\'t receive reply',
        0x04: 'Reply has wrong length',
        0x05: 'Reply has wrong CRC',
        0x06: 'Reply has wrong frame ID'
    }

    def __new__(cls, code):
        if code in cls.inst:
            return cls.inst[code]
        inst = object.__new__(cls)
        inst.__init__(code)
        cls.inst[code] = inst
        return inst

    def __init__(self, code):
        self._code = code

    @property
    def code(self) -> int:
        return self._code

    @property
    def desc(self) -> str:
        return self._desc.get(self.code, 'Unknown status')

    def __eq__(self, other) -> bool:
        return self.code == other.code

    def __repr__(self):
        return '{}: {}'.format(self.code, self.desc)


class Status:
    OK = _StatusCodes(0x00)
    REQ_ERR = _StatusCodes(0x01)
    NO_ACK = _StatusCodes(0x02)
    REPLY_ERR = _StatusCodes(0x03)
    LEN_ERR = _StatusCodes(0x04)
    CRC_ERR = _StatusCodes(0x05)
    ID_ERR = _StatusCodes(0x06)

    def __new__(cls, code) -> _StatusCodes:
        return _StatusCodes(code)
