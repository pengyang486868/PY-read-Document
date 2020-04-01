from pptapi.readppt import readpptx, readimg
from pdfapi.pdf2pic import transpic
from pdfapi import readpdf
from dwgapi import readdxf
from wordapi import readword, transdoc

import os
import config

if __name__ == '__main__':
    pptxpath = r'D:\filedata\uname\f/C-technical-05+第二节-混凝土灌注桩施工.pptx'
    # pdfpath = r'D:/data/pt.pdf'
    pdfpath = r'D:/filedata/test.pdf'
    pdftxtpath = r'D:/data/pdftxt.pdf'
    dxfpath = r'D:\filedata\uname\f/D-commercial-01+来福士T2(2-6,25-屋顶).dxf'
    # dxfpath = r'D:\filedata\uname\raw/第一层土分块22.dxf'
    wordpath = r'D:\filedata\uname\f/M-bimsys-04+杭州BIM系统.docx'
    resultdir = r'D:/result'

    username = config.test_username
    imgdir = os.path.join(config.root_dir, username, 'image-test')

    # pdftxt = readpdf.readtext(pdfpath)
    # pdftxt = readpdf.readbyocr(pdfpath)

    # curimg = readword.readimg(wordpath, imgdir, 'test')
    # curimg = readimg(pptxpath, imgdir, 'test')

    r = readdxf.split_drawing_byblock(dxfpath)

    # transtest_origin = r'D:\data\newexp-word03test.doc'
    # transtest_target = r'D:\data'
    # transdoc.doc2docx(transtest_origin, transtest_target)

    # cntarr = [1] * 5 + [3] * 3 + [11] * 4 + [12] * 6 + [13] * 48 + [14] * 24 + \
    #          [15] * 30 + [16] * 10 + [17] * 2 + [18]
    # lmin, lmax = readpdf.pdflinelen(cntarr, lenrange=4, minlen=7)
    print()
