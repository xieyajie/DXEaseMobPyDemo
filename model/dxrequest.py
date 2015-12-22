# coding = 'utf-8'

import json
import urllib.request
import urllib.parse
import urllib.error
from model.dxresponse import *


def http_request(url, headers, parameters, method):
    if len(url) == 0:
        return ''

    body_data = None
    if parameters is not None and len(parameters) > 0:
        if 'Content-Type' in headers:
            content_type = headers['Content-Type']
            if content_type == 'application/json':
                body_data = json.dumps(parameters).encode('utf-8')
        else:
            body_data = urllib.parse.urlencode(parameters).encode('utf-8')

    req = urllib.request.Request(url, body_data, headers, method)

    if method == 'PUT' or method == 'DELETE':
        req.get_method = lambda: method

    code = 0
    des = ''
    respdata = None
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as error:
        code = error.code
        des = error.reason
    except urllib.error.URLError as error:
        code = error.code
        des = error.reason
    else:
        respdata = response.read().decode('utf-8')
        print(respdata)
        if 'Accept' in headers:
            accept = headers['Accept']
            if accept == 'application/json':
                respdata = json.loads(respdata)

    tmp = DXResponse(code, des, respdata)
    return tmp


def get(url, headers, parameters=None):
    return http_request(url, headers, parameters, 'GET')


def post(url, headers, parameters=None):
    return http_request(url, headers, parameters, 'POST')


def put(url, headers, parameters=None):
    return http_request(url, headers, parameters, 'PUT')


def delete(url, headers, parameters=None):
    return http_request(url, headers, parameters, 'DELETE')
