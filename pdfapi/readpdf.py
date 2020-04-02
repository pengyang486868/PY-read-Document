import pdfplumber
from collections import Counter
from ocrapi import baidu as ocr
import config
import os, uuid

from .pdf2pic import transpic


# can extract text fields
def readtext(full_path):
    result = []
    with pdfplumber.open(full_path) as pdf:
        for p in pdf.pages:
            text = p.extract_text()
            if not text:
                continue
            # table = page.extract_tables()
            textarr = text.split('\n')
            result = result + textarr

    if len(result) < 10:
        return result

    # 还需猜测文档一般行字数 合并句尾分段
    cntarr = list(map(len, result))
    minlen, maxlen = pdflinelen(cntarr)
    result = combine_normal_line(result, minlen, maxlen)

    return result


# to pics then ocr
def readbyocr(full_path):
    tempdir = os.path.join(config.root_dir, config.test_username, 'temp', str(uuid.uuid4()))
    os.mkdir(tempdir)
    transpic(full_path, resultdir=tempdir)

    result = []
    pics = os.listdir(tempdir)
    pics.sort(key=lambda x: int(os.path.splitext(x)[0]))
    for p in pics:
        result += ocr.img_to_str(os.path.join(tempdir, p))
        print(p)

    # 还需猜测文档一般行字数 合并句尾分段
    cntarr = list(map(len, result))
    minlen, maxlen = pdflinelen(cntarr)
    result = combine_normal_line(result, minlen, maxlen)
    return result


# combine normal according to normal range
def combine_normal_line(lines, minlen, maxlen):
    back = 0
    front = 0
    length = len(lines)
    result = []

    while True:
        # if current is not normal
        if len(lines[front]) < minlen or len(lines[front]) > maxlen:
            result.append(lines[front])
            front += 1
            if front == length:
                break
            back = front
            continue

        # if current is normal, can decide next
        front += 1
        if front < length and (len(lines[front]) < minlen or len(lines[front]) > maxlen):
            # link to the end
            if front == length:
                result.append(''.join(lines[back:front]))
                break
            result.append(''.join(lines[back:front + 1]))
            front += 1
            back = front

        # exit
        if front == length:
            break
    return result


# guess the normal length range of lines
def pdflinelen(arr, lenrange=6, minlen=10):
    cntor = Counter(arr)
    for i in range(minlen):
        if i in cntor:
            del cntor[i]  # delete very short lines

    key = cntor.keys()
    tmax = max(key)
    tmin = min(key)

    # exit: but practically not possible
    if tmax - tmin < lenrange:
        return tmin, tmax

    maxcount = 0
    for i in range(lenrange):
        maxcount += cntor[tmin + i]

    min_result = tmin
    lastcount = maxcount
    for c in range(tmin + 1, tmax - lenrange + 2):
        curcount = lastcount - cntor[c - 1] + cntor[c + lenrange - 1]
        if curcount > maxcount:
            maxcount = curcount
            min_result = c
        lastcount = curcount

    return min_result, min_result + lenrange - 1
