# -*- coding: utf-8 -*-
import os
import sys
import codecs
import json
import time
from time import *
import logging

# pip install django
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.template.loader import render_to_string

# pip install ws4py
from ws4py.client.threadedclient import WebSocketClient

from markerstorage import markerstorage_settings
from .models import DemoMarker

formatter = logging.Formatter(markerstorage_settings.LOG_FORMAT)
h = logging.FileHandler(markerstorage_settings.LOG_PATH)
h.setFormatter(formatter)

logger = logging.getLogger(markerstorage_settings.APP_NAME)
logger.setLevel(markerstorage_settings.LOG_LEVEL)
logger.addHandler(h)


def error500(request):
    return render_to_response('500.html', {})


def error404(request):
    return render_to_response('404.html', {})


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = json.dumps(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def convert_dict_demoarker(o):
    _a = {'id': o.id,
          'create_dt': o.create_dt.isoformat(),
          'update_dt': o.update_dt.isoformat(),
          'name': o.name,
          'x': o.x,
          'y': o.y,
          'auther': o.auther,
          'desc': o.desc,
          'memo': o.memo}

    return _a


def convert_dict_demoarkers(qs):
    _datas = []

    for o in qs:
        _a = {'id': o.id,
              'create_dt': o.create_dt.isoformat(),
              'update_dt': o.update_dt.isoformat(),
              'name': o.name,
              'x': o.x,
              'y': o.y,
              'auther': o.auther,
              'desc': o.desc,
              'memo': o.memo}
        _datas.append(_a)

    return _datas


@csrf_exempt
def markerdata_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        _qs = DemoMarker.objects.all().order_by('-pk')
        _datas = convert_dict_demoarkers(_qs)
        return JSONResponse(_datas)
    else:
        _qs = DemoMarker.objects.all().order_by('-pk')
        _datas = convert_dict_demoarkers(_qs)
        return JSONResponse(_datas)


@csrf_exempt
def markerdata_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    demomarker = None

    if request.method == 'GET':
        try:
            _o = DemoMarker.objects.get(pk=pk)
        except DemoMarker.DoesNotExist:
            return HttpResponse(status=404)

        _data = convert_dict_demoarker(_o)
        return JSONResponse(_data)

    elif request.method == 'POST':
        logger.debug('POST (pk=%s)' % pk)

        # check password
        try:
            _pass = request.GET.get('password', '')

            if _pass != markerstorage_settings.REST_PUT_PASSWORD:
                return JSONResponse('', status=401)
        except:
            logger.warn('EXCEPT: fail password. (%s)' % sys.exc_info()[1])
            return JSONResponse('', status=401)

        # insert or update
        try:
            _s = request.body.decode('utf-8')
            data = json.loads(_s)
            logger.debug(data)

            if int(pk) < 1:
                logger.info('do insert')
                created = DemoMarker(id=None,
                                     create_dt=data['create_dt'],
                                     update_dt=data['update_dt'],
                                     name=data['name'],
                                     x=data['x'],
                                     y=data['y'],
                                     auther=data['auther'],
                                     desc=data['desc'],
                                     memo=data['memo'])
                created.save()

                data['id'] = '%d' % (created.id)

                # send websocket message
                pushdata = [data]
                notify_websocket(pushdata)

                _status = 201
                _data = data
            else:
                logger.info('do update')
                o = DemoMarker.objects.get(pk=pk)

                o.update_dt = data['update_dt']
                o.name = data['name']
                o.x = data['x']
                o.y = data['y']
                o.auther = data['auther']
                o.desc = data['desc']
                o.memo = data['memo']

                o.save()

                pushdata = [json.dumps(convert_dict_demoarker(o))]
                notify_websocket(pushdata)

                _status = 200
                _data = data
        except DemoMarker.DoesNotExist:
            return HttpResponse(status=404)
        except:
            logger.warn('EXCEPT: fail request data parse. (%s)' %
                        sys.exc_info()[1])
            return JSONResponse('{}', status=400)

        return JSONResponse(data=_data, status=_status)


    #elif request.method == 'DELETE':
    #    snippet.delete()
    #    return HttpResponse(status=204)


def osm_index(request):
    return my_render_to_response(request,
                                 'osm/index.html',
                                 {'key1': 'value1'})


def osm_first(request):
    return my_render_to_response(
        request,
        'osm/ol2/first.html',
        {'key1': 'value1'})


def osm_marker1(request):
    return my_render_to_response(
        request,
        'osm/ol2/marker1.html',
        {'key1': 'value1'})


def osm_marker2(request):
    return my_render_to_response(
        request,
        'osm/ol2/marker2.html',
        {'initialmarker_url': '/markerstorage/osm/ol2/marker2.json'}
        )


def osm_marker2_json(request):
    return my_render_to_response(
        request,
        'osm/ol2/marker2.json',
        {'key1': 'value1'}
        )


def osm_marker3(request):
    ip = get_client_ip(request)
    if -1 < ip.find("192.168.22."):
        wspush_url = markerstorage_settings.WSPUSH_URL_INTRA
    else:
        wspush_url = markerstorage_settings.WSPUSH_URL

    return my_render_to_response(
        request,
        'osm/ol2/marker3.html',
        {'initialmarker_url': markerstorage_settings.INITIALMARKER_URL,
         'wspush_url': wspush_url,
         'wspush_recvtoken': markerstorage_settings.WSPUSH_RECVTOKEN,
         })


def osm_tile1(request):
    return my_render_to_response(
        request,
        'osm/ol2/tile1.html',
        {'key1': 'value1'})


def osm_tile1_image(request, tile_ver, tile_z, tile_x, tile_y):
    response = HttpResponse()
    response['Content-Type'] = 'image/png'

    try:
        filepath = '%s/static/images/%s' % (
            markerstorage_settings.APP_ROOT,
            'tiletest.png')
        with open(filepath, 'rb') as f:
            response.write(f.read())
    except:
        print(("EXCEPT: %s" % (sys.exc_info()[1])))

    return response


def osm_ol5_first(request):
    return my_render_to_response(
        request,
        'osm/ol5/first.html',
        {'key1': 'value1'})


def osm_ol5_marker1(request):
    return my_render_to_response(
        request,
        'osm/ol5/marker1.html',
        {'key1': 'value1'})

def my_render_to_response(request, template_file, paramdict):
    response = HttpResponse()
    paramdict['mount_prefix'] = markerstorage_settings.MOUNT_PREFIX

    _gen_html = render_to_string(template_file,
                                 context=paramdict,
                                 request=request)
    response.write(_gen_html)
    return response


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class DummyClient(WebSocketClient):
    _is_auth = -1

    def opened(self):
        senddata = {'func': 'auth',
                    'param': {
                        'token': markerstorage_settings.WSPUSH_SENDTOKEN}
                    }
        self.send(json.dumps(senddata).encode())

    def closed(self, code, reason):
        logger.info(
            "Websocket server to Closed down. (code=%s,reason=%s" %
            (code, reason))

    def received_message(self, m):
        try:
            convjson = json.loads(m.data.decode())
            logger.info('message received: %s' % convjson)

            if convjson['func'] == 'auth':
                if convjson['statuscode'] == '200':
                    self._is_auth = 1
                    logger.info('success auth websocket server.')
                else:
                    self._is_auth = 0
                    logger.warn('fail auth websocket server.')
            else:
                pass
        except:
            logger.error('EXCEPT: recv msg (%s)' % sys.exc_info()[1])

    def sendmsg(self, markertype, markerlist):
        senddata = {'func': 'broadcast_msg',
                    'param': {'markertype': markertype,
                              'markerlist': markerlist}
                    }
        logger.info(senddata)
        self.send(json.dumps(senddata).encode())

    def is_auth(self):
        return self._is_auth


def notify_websocket(datalist):
    logger.debug('IN notify_websocket()')
    count = 0

    try:
        ws = DummyClient(markerstorage_settings.WSPUSH_URL_INTRA,
                         protocols=['http-only', 'chat'])
        ws.connect()

        while(count < markerstorage_settings.WSPUSH_POLLING_WAIT_MAXCOUNT):
            if ws.is_auth() < 0:
                sleep(markerstorage_settings.WSPUSH_POLLING_WAIT_SPAN)
                count = count + 1
            elif 0 == ws.is_auth():
                raise('fail auth websocket server.')
            else:
                ws.sendmsg('testobject1', datalist)
                logger.info('success notify websocket.')
                ws.close()
                break
    except:
        logger.error('EXCEPT: fail send websocket message (%s)' %
                     sys.exc_info()[1])
        return 1

    return 0
