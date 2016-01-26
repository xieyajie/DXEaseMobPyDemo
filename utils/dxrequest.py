# coding = 'utf-8'

import json
import urllib.request
import urllib.parse
import urllib.error
import time
import mimetypes

from utils.dxresponse import *


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
        respdata = response.read().decode('utf-8')
        print(respdata)
        if 'Accept' in headers:
            accept = headers['Accept']
            if accept == 'application/json':
                respdata = json.loads(respdata)
    except urllib.error.HTTPError as err:
        code = err.code
        des = err.reason
    except urllib.error.URLError as err:
        code = -1
        des = err.reason

    tmp = DXResponse(code, des, respdata)
    return tmp


def get(url, headers, parameters=None):
    return http_request(url, headers, parameters, 'GET')


def post(url, headers, parameters=None, files=None):
    if files is None:
        return http_request(url, headers, parameters, 'POST')
    else:
        req = urllib.request.Request(url, files.encode('ISO-8859-1'))
        req.add_header()
        try:
            resp = urllib.request.urlopen(req)
            body = resp.read().decode('utf-8')
            print(body)
        except urllib.error.HTTPError as e:
            print(e.fp.read())


def put(url, headers, parameters=None):
    return http_request(url, headers, parameters, 'PUT')


def delete(url, headers, parameters=None):
    return http_request(url, headers, parameters, 'DELETE')


def _encode_multipart(params_dict):

    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    for k, v in params_dict.items():
        data.append('--%s' % boundary)

        if hasattr(v, 'read'):
            filename = getattr(v, 'name', '')
            content = v.read()
            decoded_content = content.decode('ISO-8859-1')
            data.append('Content-Disposition: form-data; name="%s"; filename="hidden"' % k)
            data.append('Content-Type: application/octet-stream\r\n')
            data.append(decoded_content)
        else:
            data.append('Content-Disposition: form-data; name="%s"\r\n' % k)
            data.append(v if isinstance(v, str) else v.decode('utf-8'))

        data.append('--%s--\r\n' % boundary)

    return '\r\n'.join(data), boundary


def upload_file(url, file_path, headers):
    params = {'file': open(file_path, "rb")}
    datagen, boundary = _encode_multipart(params)
    req = urllib.request.Request(url, datagen.encode('ISO-8859-1'))

    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    for key in headers:
        req.add_header(key, headers[key])

    code = 0
    des = ''
    respdata = ''
    try:
        resp = urllib.request.urlopen(req)
        respdata = resp.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        code = -1
        des = e.reason
        respdata = e.fp.read()

    tmp = DXResponse(code, des, respdata)
    return tmp
