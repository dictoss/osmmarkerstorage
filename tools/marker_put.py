#!/usr/bin/env python
import sys
import json
import datetime
import time
import requests

MP_URL = 'http://192.168.22.102:8000/markerstorage/markerdata/0/'
#MP_URL = 'http://192.168.22.30/osmproj1/markerstorage/markerdata/0/'
MP_POST_PASS = 'qWjJjNeiv.Bvc'


def put_markerobject():
    _seq = 0

    payload = {'id': _seq,
               'create_dt':  datetime.datetime.now().isoformat(),
               'update_dt':  datetime.datetime.now().isoformat(),
               'name': 'object_test',
               'x': '142.370',
               'y': '43.765',
               'auther': 'dictoss',
               'desc': 'test messge'}

    try:
        query_args = {'password': MP_POST_PASS}
        header_args = {'Content-Type': 'application/json; charset=utf-8'}

        print('try send PUT request.')
        r = requests.post(MP_URL,
                          params=query_args,
                          headers=header_args,
                          data=json.dumps(payload).encode())

        print(('status code: %s' % (r.status_code)))
        print(r.text)
    except:
        print(('EXCEPT: fail PUT (%s)' % sys.exc_info()[1]))

    return


def main():
    put_markerobject()
    return 0


if __name__ == '__main__':
    ret = main()
    sys.exit(ret)
