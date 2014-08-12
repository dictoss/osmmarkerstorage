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
                    'param': {'token': 'abcdefgh'}
                    }
        self.send(json.dumps(senddata))
        print(senddata)

    def closed(self, code, reason):
        print "Closed down", code, reason

    def received_message(self, m):
        print "=> %d %s" % (len(m), str(m))
        if len(str(m)) == 175:
            self.close(reason='Bye bye')

    def sendmsg(self):
        _seq = 1000

        senddata = {'func': 'broadcast_msg',
                    'param': {'markertype': 'testobject1', 
                              'markerlist': [
                    {'id': _seq,
                     'create_dt':  datetime.datetime.now().isoformat(),
                     'update_dt':  datetime.datetime.now().isoformat(),
                     'name': 'object%d' % (_seq),
                     'x': '142.370',
                     'y': '43.765',
                     'auther': 'dictoss',
                     'desc': 'test messge'}
                    ]
                              }
                    }
        self.send(json.dumps(senddata))
        print(senddata)


def main():
    try:
        ws = DummyClient('ws://192.168.22.102:8888/',
                         protocols=['http-only', 'chat'])
        ws.connect()

        while True:
            line = raw_input()
            print("stdin!")
            ws.sendmsg()

    except KeyboardInterrupt:
        ws.close()
        return 0
    except:
        print("EXCEPT: %s" % sys.exc_info()[1])
        return 1


if __name__ == '__main__':
    ret = main()
    sys.exit(ret)
