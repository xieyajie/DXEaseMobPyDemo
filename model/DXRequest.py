#coding = 'utf-8'

__author__ = 'xieyajie'

import json
import urllib.request
import urllib.parse
from model.DXResponse import *

def httpRequest(aUrl, aHeaders, aParameters, aMethod):
    if len(aUrl) == 0:
        return ''

    bodyData = None
    if aParameters != None and len(aParameters) > 0:
        if 'Content-Type' in aHeaders:
            contentType = aHeaders['Content-Type']
            if contentType == 'application/json':
                bodyData = json.dumps(aParameters).encode('utf-8')
        else:
            bodyData = urllib.parse.urlencode(aParameters).encode('utf-8')

    req = urllib.request.Request(aUrl, bodyData, aHeaders, aMethod)

    if aMethod == 'PUT' or aMethod == 'DELETE':
        req.get_method = lambda:aMethod

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
        if 'Accept' in aHeaders:
            accept = aHeaders['Accept']
            if accept == 'application/json':
                respdata = json.loads(respdata)

    tmp = DXResponse(code, des, respdata)
    return tmp

def get(aUrl, aHeaders, aParameters = None):
    return httpRequest(aUrl, aHeaders, aParameters, 'GET')

def post(aUrl, aHeaders, aParameters = None):
    return httpRequest(aUrl, aHeaders, aParameters, 'POST')

def put(aUrl, aHeaders, aParameters = None):
    return httpRequest(aUrl, aHeaders, aParameters, 'PUT')

def delete(aUrl, aHeaders, aParameters = None):
    return httpRequest(aUrl, aHeaders, aParameters, 'DELETE')