from txtapi import readtxt
from wordapi import readword, transdoc
from pptapi import readppt, transppt
from pdfapi import readpdf
import utils
import config


def transform(fpath, tdir, extname):
    if extname == '.doc':
        transdoc.doc2docx(fpath, tdir, remove=False)
        return True
    if extname == '.ppt':
        transppt.ppt2pptx(fpath, tdir, remove=False)
        return True
    return False


def analysis(fpath, extname):
    content = None
    kw = []
    farr = []

    # do extract below
    if extname == '.txt':
        content = readtxt.read(fpath)

    if extname == '.docx':
        content = readword.readtxt(fpath)
    if extname == '.doc':
        content = readword.readtxt(fpath + 'x')

    if extname == '.pptx':
        content = readppt.readtxt(fpath)
    if extname == '.ppt':
        content = readppt.readtxt(fpath + 'x')

    if extname == '.pdf':
        content = readpdf.readtext(fpath)

    # do analysis
    if content is not None:
        kw = utils.get_keywords(content, config.kw_topk)
        freq = utils.get_freq(content)
        farr = list(map(lambda x: str(freq[x]) if x in freq else 0, kw))

    return ','.join(kw), ','.join(farr)
