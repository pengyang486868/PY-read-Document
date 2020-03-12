import urllib.request as rq
from urllib.parse import quote
import re


# https://baike.baidu.com/search?word=%E6%B7%B7%E5%87%9D%E5%9C%9F
def search(word):
    url = r'https://baike.baidu.com/search?rn=3&word=' + quote(word)
    req = rq.Request(url)  # , headers={'Authorization': token}
    f = rq.urlopen(req)
    responsedata = str(f.read().decode())
    # <a class="result-title" href="..." target="_blank"><em>混凝土</em>_百度百科</a>
    umatch = re.compile(r'<a class="result-title" href="(.*)" target="_blank">')
    usearch = umatch.findall(responsedata)
    if len(usearch) > 0:
        return usearch[0]
    return None


def retrieve(url):
    req = rq.Request(url)  # , headers={'Authorization': token}
    f = rq.urlopen(req)
    responsedata = str(f.read().decode())

    # section title
    # <div class="para-title level-2" label-module="para-title">
    # <h2 class="title-text"><span class="title-prefix">混凝土</span>功能作用</h2>

    # subsection title
    # <div class="para-title level-3" label-module="para-title">
    # <h3 class="title-text"><span class="title-prefix">混凝土</span>和易性</h3></div>

    # paragraph
    # <div class="para" label-module="para">...</div>

    # match re
    # paramatch = re.compile(r'<div class="para" label-module="para">(.*)</div>')
    # paras = paramatch.findall(responsedata)
    allmatch = re.compile(
        r'(?:<div class="para-title level-2" label-module="para-title">\n'
        r'<h2 class="title-text"><span class="title-prefix">.*</span>(.*)</h2>' +
        r'|<div class="para-title level-3" label-module="para-title">\n'
        r'<h3 class="title-text"><span class="title-prefix">.*</span>(.*)</h3>' +
        r'|<div class="para" label-module="para">(.*)</div>)')
    allp = allmatch.findall(responsedata)
    return allp  # 3 element tuple


if __name__ == '__main__':
    target = search('混凝土')
    if target:
        content = retrieve(target)
