#coding = 'utf-8'

__author__ = 'xieyajie'

import json
import urllib.request
import urllib.parse
from model.dx_response import *

def http_request(url, headers, parameters, method):
    if len(url) == 0:
        return ''

    bodyData = None
    if parameters != None and len(parameters) > 0:
        if 'Content-Type' in headers:
            contentType = headers['Content-Type']
            if contentType == 'application/json':
                bodyData = json.dumps(parameters).encode('utf-8')
        else:
            bodyData = urllib.parse.urlencode(parameters).encode('utf-8')

    req = urllib.request.Request(url, bodyData, headers, method)

    if method == 'PUT' or method == 'DELETE':
        req.get_method = lambda:method

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

def get(url, headers, parameters = None):
    return http_request(url, headers, parameters, 'GET')

def post(url, headers, parameters = None):
    return http_request(url, headers, parameters, 'POST')

def put(url, headers, parameters = None):
    return http_request(url, headers, parameters, 'PUT')

def delete(url, headers, parameters = None):
    return http_request(url, headers, parameters, 'DELETE')