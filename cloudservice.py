import json
from urllib import request, parse
import config
import numpy as np
import re


# general GET
def get_action(url: str, pdic=None):
    if pdic:
        for key, val in pdic:
            url += key + '=' + val + '&'
    url = url.strip('&')
    req = request.Request(url, headers={'Authorization': config.token})
    f = request.urlopen(req)
    cdata = str(f.read().decode())
    return json.loads(cdata)


# general POST
def post_action(url, pdic):
    if not pdic:
        params = None
    else:
        params = json.dumps(pdic).encode('utf-8')
    headers = {'Accept-Charset': 'utf-8', 'Content-Type': 'application/json',
               'Authorization': config.token}
    req = request.Request(url=url, data=params, headers=headers, method='POST')
    response = request.urlopen(req).read()
    return json.loads(response)


# general DELETE
def delete_action(url, pdic):
    if not pdic:
        params = None
    else:
        params = json.dumps(pdic).encode('utf-8')
    headers = {'Accept-Charset': 'utf-8', 'Content-Type': 'application/json',
               'Authorization': config.token}
    req = request.Request(url=url, data=params, headers=headers, method='DELETE')
    response = request.urlopen(req).read()
    return True


# general PUT
def put_action(url, pdic):
    if not pdic:
        params = None
    else:
        params = json.dumps(pdic).encode('utf-8')
    headers = {'Accept-Charset': 'utf-8', 'Content-Type': 'application/json',
               'Authorization': config.token}
    req = request.Request(url=url, data=params, headers=headers, method='PUT')
    response = request.urlopen(req).read()
    return True


def get_documenttask():
    url = config.backendserver + '/api/projects/0/entities/documenttask'
    response = get_action(url)
    return response


def download_doc(docurl, path):
    request.urlretrieve(docurl, path)
    return True


def get_doctag():
    url = config.backendserver + '/api/projects/0/document/filetags'
    response = get_action(url)
    return response


def create_doctag(tag):
    url = config.backendserver + '/api/projects/0/document/filetags'
    url = url + '?tagName=' + parse.quote(tag)
    response = post_action(url, None)
    return response


def delete_doctag(tagid):
    url = config.backendserver + '/api/projects/0/document/filetags'
    url = url + '?tagId=' + str(tagid)
    response = delete_action(url, None)
    return response


def create_doctagrel(pairs):
    url = config.backendserver + '/api/projects/0/document/files/tags'
    params = []
    for pair in pairs:
        params.append({'fileId': pair[0], 'tagId': pair[1]})
    response = put_action(url, params)
    return True
