import json
from urllib import request, parse
import config
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import re, os


def is_pure_abc(s, number_as_abc=False):
    lowbound = 65
    if number_as_abc:
        lowbound = 48
    charr = [',', '.', '-', ' ', '\\', '@', '%']
    for ch in s:
        c = ord(ch)  # ascii
        if (c > 122 or c < lowbound) and (ch not in charr):
            return False
    return True


def remove_cadliteral(s):
    # {\xxx;TEXT} -> TEXT
    result = re.sub(r'{\\(?P<control>.+?);(?P<txt>.+?)}', r'\g<txt>', s)

    # delete \H1.3333x;
    result = re.sub(r'\\H.+?x', r'', result)

    # delete \pi-7999.9,l7999.9;
    result = re.sub(r'\\pi-.+?;', r'', result)

    # delete \\A1;
    result = re.sub(r'\\\\A1;', r'', result)

    # \P and space
    minlen = 8
    temp = re.sub(r'\s+', r'', result)
    if len(temp) <= minlen:
        result = temp
    else:
        result = re.sub(r'\\P', r' ', result)
        result = re.sub(r'\s+', r' ', result)

    # %%...
    result = re.sub(r'%%', r'', result)

    return result


# \n ' '
def remove_blank(s: str) -> str:
    result = re.sub(r'\s+', r'', s)
    result = re.sub(r'\n', r'', result)
    return result


# string similarity
def str_similar(s1: str, s2: str) -> float:
    if len(s1) < 1 or len(s2) < 1:
        return 0
    if s1 in s2:
        return len(s1) / len(s2)
    if s2 in s1:
        return len(s2) / len(s1)
    return 0


# plot simple
def plotxy(xall, yall, zall, clsarr):
    marks = ['o', 'v', 'd', 's', '*', '+', 'h', 'x', 'D', '4']
    allcls = list(set(clsarr))
    data = list(zip(xall, yall, zall, clsarr))
    fig = plt.figure()
    ax = Axes3D(fig)
    for indx, curcls in enumerate(allcls):
        curdata = np.array(list(map(list, filter(lambda x: x[3] == curcls, data))))
        ax.scatter(curdata[:, 0], curdata[:, 1], curdata[:, 2], label=str(curcls), marker=marks[indx], s=80)

    plt.legend()
    plt.show()


def get_action(url: str, pdic=None):
    if pdic:
        for key, val in pdic:
            url += key + '=' + val + '&'
    url = url.strip('&')
    req = request.Request(url, headers={})
    f = request.urlopen(req)
    cdata = str(f.read().decode())
    return json.loads(cdata)


def post_action(url, pdic):
    params = json.dumps(pdic).encode('utf-8')
    headers = {'Accept-Charset': 'utf-8', 'Content-Type': 'application/json'}
    req = request.Request(url=url, data=params, headers=headers, method='POST')
    response = request.urlopen(req).read()
    return json.loads(response)


def get_keywords(t, n=10):
    url = config.nlpserver + '/keyw/words'
    params = {'wn': n, 't': t}
    response = post_action(url, params)
    return response['result']


def get_keywordsmany(t, n=10):
    url = config.nlpserver + '/keyw/wordsmany'
    params = {'wn': n, 't': t}
    response = post_action(url, params)
    return response['result']


def get_freq(t):
    url = config.nlpserver + '/cut/freq'
    params = {'t': t}
    response = post_action(url, params)
    return response['result']


def get_phrase(t, n=10):
    url = config.nlpserver + '/keyw/phrases'
    params = {'wn': n, 't': t}
    response = post_action(url, params)
    return response['result']


def get_newwords(t, n=10):
    url = config.nlpserver + '/keyw/newwords'
    params = {'wn': n, 't': t}
    response = post_action(url, params)
    return response['result']


def get_summary(t, n=5):
    url = config.nlpserver + '/summary/auto'
    params = {'wn': n, 't': t}
    response = post_action(url, params)
    return response['result']


def get_namedwords(t):
    url = config.nlpserver + '/keyw/namedwords'
    params = {'t': t}
    response = post_action(url, params)
    return response['result']


def is_company_str(s) -> bool:
    magicstr = '是一个好单位'
    url = config.nlpserver + '/keyw/iscompany?'
    params = {'w': s + magicstr}
    response = get_action(url, params)
    return response['result']


def is_company_many(arr):
    magicstr = '是一个好单位'
    url = config.nlpserver + '/keyw/iscompanymany'
    params = {'t': [s + magicstr for s in arr]}
    response = post_action(url, params)
    return response['result']
