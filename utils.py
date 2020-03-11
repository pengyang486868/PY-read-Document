import json
from urllib import request, parse
import config


def is_pure_abc(s):
    charr = [',', '.', '-', ' ']
    for ch in s:
        c = ord(ch)  # ascii
        if (c > 122 or c < 48) and (ch not in charr):
            return False
    return True


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
