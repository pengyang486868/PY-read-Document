import json
from urllib import request, parse
import config


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


def get_documenttask(projid=0):
    url = config.backendserver + '/api/projects/{}/entities/documenttask'.format(projid)
    response = get_action(url)
    return response


def download_doc(docurl, path):
    request.urlretrieve(docurl, path)
    return True


def get_doctag(projid=0):
    url = config.backendserver + '/api/projects/{}/document/filetags'.format(projid)
    response = get_action(url)
    return response


def create_doctag(tag, projid=0):
    url = config.backendserver + '/api/projects/{}/document/filetags'.format(projid)
    url = url + '?tagName=' + parse.quote(tag)
    response = post_action(url, None)
    return response


def delete_doctag(tagid, projid=0):
    url = config.backendserver + '/api/projects/{}/document/filetags'.format(projid)
    url = url + '?tagId=' + str(tagid)
    response = delete_action(url, None)
    return response


def create_doctagrel(pairs, projid=0):
    url = config.backendserver + '/api/projects/{}/document/files/tags'.format(projid)
    params = []
    for pair in pairs:
        params.append({'fileId': pair[0], 'tagId': pair[1]})
    response = put_action(url, params)
    return True


def delete_doctagrel(relid, projid=0):
    url = config.backendserver + '/api/projects/{}/document/files/tags'.format(projid)
    url = url + '?fileTagId=' + str(relid)
    response = delete_action(url, None)
    return response


def change_step(taskid, data: dict, projid=0):
    url = config.backendserver + '/api/projects/{}/entities/documenttask/{}'.format(projid, taskid)
    params = data
    response = put_action(url, params)
    return True


def get_docs_byid(fid, projid=0):
    # url = config.backendserver + '/api/projects/{}/document/files/{}'.format(projid, fid)
    url = config.backendserver + '/api/projects/{}/entities/documentfile/{}'.format(projid, fid)
    response = get_action(url)
    return response


def fill_docinfo(docid, data: dict, projid=0):
    # url = config.backendserver + '/api/projects/{}/document/files?id={}'.format(projid, docid)
    url = config.backendserver + '/api/projects/{}/entities/documentfile/{}'.format(projid, docid)
    params = data
    response = put_action(url, params)
    return True


def get_all_projs():
    url = config.backendserver + '/api/projects/all'
    response = get_action(url)
    return response


def get_file_projs():
    url = config.backendserver + '/api/projects/0/entities/documenttask'
    response = get_action(url)
    return set([x['projectId'] for x in response])


def add_file(data, projid=0):
    url = config.backendserver + '/api/projects/{}/document/files'.format(projid)
    params = data
    response = post_action(url, params)
    return True


def add_dir(name, parentid, projid=0):
    url = config.backendserver + '/api/projects/{}/document/directory'.format(projid)
    params = {
        "name": name,
        "parentId": parentid,
        "creatorId": 1
    }
    response = post_action(url, params)
    return True


def get_dir_subs(dirid, projid=0):
    url = (config.backendserver +
           '/api/projects/{}/document/directory?currentDirectoryId={}'.format(projid, dirid))
    response = get_action(url)
    return response
