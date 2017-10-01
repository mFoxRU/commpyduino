#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'mFoxRU'

import json

import paho.mqtt.client as mqtt

from commpyduino.connector import Connector
from commpyduino.status_codes import _StatusCodes


class SCEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, _StatusCodes):
            return [o.code, o.desc]


class Translator:

    req = 'home/req'
    rep = 'home/rep'

    def __init__(self, connector):
        self.con = connector
        self.client = mqtt.Client('pcd', userdata='me')

        def on_connect(client, userdata, flags, rc):
            client.subscribe(self.req)

        def on_message(client, userdata, msg):
            reply = self.communicate(json.loads(msg.payload))
            client.publish(self.rep, json.dumps(reply, cls=SCEncoder))

        self.client.on_connect = on_connect
        self.client.on_message = on_message

    def start(self):
        self.client.connect("127.0.0.1", 1883, 60)
        self.client.loop_forever()

    def communicate(self, payload):
        cmd = payload['cmd']
        args = payload['values']
        command = self.con.commands.get(cmd, None)
        if command is None:
            return {'status': (-1, 'Invalid command')}
        return command(*args)


if __name__ == '__main__':
    con = Connector('COM6')
    translator = Translator(con)
    translator.start()


