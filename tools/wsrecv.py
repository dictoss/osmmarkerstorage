#!/usr/bin/python
#
import sys
import json
import datetime
import time
from ws4py.client.threadedclient import WebSocketClient


class DummyClient(WebSocketClient):
    def opened(self):
        senddata = {'func': 'auth',
                    'param': {'token': '12345678'}
                    }
        self.send(json.dumps(senddata))
        print(senddata)

    def closed(self, code, reason):
        print("Closed down %s %s" % (code, reason))

    def received_message(self, m):
        print("=> %d %s" % (len(m), str(m)))
        print
        if len(str(m)) == 175:
            self.close(reason='Bye bye')

if __name__ == '__main__':
    print("let's go receiver.")

    try:
        ws = DummyClient('ws://192.168.22.102:8888/',
                         protocols=['http-only', 'chat'])
        ws.connect()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        ws.close()
