from txtapi import readtxt
import utils


def analysis(fpath, extname):
    # content = None
    kw = []
    farr = []
    if extname == '.txt':
        content = readtxt.read(fpath)
        kw = utils.get_keywords(content, 20)
        freq = utils.get_freq(content)
        farr = list(map(lambda x: str(freq[x]) if x in freq else 0, kw))

    return ','.join(kw), ','.join(farr)
