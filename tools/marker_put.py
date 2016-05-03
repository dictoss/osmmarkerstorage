#!/usr/bin/python3
import sys
import json
import datetime
import time
import urllib.request
import urllib.parse
import urllib.error

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
        encode_url_param = urllib.parse.urlencode(query_args)

        req = urllib.request.Request('%s?%s' % (MP_URL, encode_url_param))
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.method = 'POST'
        req.data = json.dumps(payload).encode()

        r = urllib.request.urlopen(req)
        print('send PUT request.')
        print(('status code: %s' % (r.code)))
    except:
        print(('EXCEPT: fail PUT (%s)' % sys.exc_info()[1]))

    return


def main():
    put_markerobject()
    return 0


if __name__ == '__main__':
    ret = main()
    sys.exit(ret)
