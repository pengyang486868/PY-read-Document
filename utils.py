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


def get_freq(t):
    url = config.nlpserver + '/cut/freq'
    params = {'t': t}
    response = post_action(url, params)
    return response['result']
