#coding = 'utf-8'

__author__ = 'xieyajie'

import json
import urllib.request
import urllib.parse
from EMHttpResponse import *

def httpRequest(aUrl, aHeaders, aParameters, aMethod):
    if len(aUrl) == 0:
        return ''

    bodyData = None
    if aParameters is not None and len(aParameters) > 0:
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
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.HTTPError as error:
        code = error.code
        respdata = error.reason
    except urllib.error.URLError as error:
        code = error.code
        respdata = error.reason
    else:
        respdata = response.read().decode('utf-8')
        print(respdata)
        if 'Accept' in aHeaders:
            accept = aHeaders['Accept']
            if accept == 'application/json':
                respdata = json.loads(respdata)

    tmp = EMHttpResponse(code, respdata)
    return tmp