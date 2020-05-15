from pptapi.readppt import readpptx, readimg,readnotes
from pdfapi.pdf2pic import transpic
from pdfapi import readpdf
from dwgapi import readdxf
from wordapi import readword, transdoc
import numpy as np

import os
import config

if __name__ == '__main__':
    pptxpath = r'D:\qqsave\854525261\FileRecv\医院建筑bim运维与智能决策系统研究与应用-中施企协科技进步奖申报.pptx'
    # pptxpath = r'D:\filedata\uname\f/C-technical-05+第二节-混凝土灌注桩施工.pptx'
    pdfpath = r'E:\contract.pdf'
    # pdfpath = r'D:/filedata/uname\f\M-bimsys-11+广联达BIM体系.pdf'
    pdftxtpath = r'D:/data/pdftxt.pdf'

    # dxfpath = r'D:\filedata\uname\dwg/D-commercial-01+来福士T2-min.dxf'
    dxfpath = r'D:\filedata\uname\儿童医院电气-min.dxf'

    wordpath = r'D:\filedata\uname\f/M-bimsys-04+杭州BIM系统.docx'

    resultdir = r'D:/result'

    username = config.test_username
    imgdir = os.path.join(config.root_dir, username, 'image-test')

    # r = readimg(pptxpath, resultdir, save_prefix='XXB-')
    r = readnotes(pptxpath)

    # pdftxt = readpdf.readtext(pdfpath)
    # print(pdftxt)
    # pdftxt = readpdf.readtext(pdfpath)
    # print(pdftxt)
    # np.savetxt(os.path.join(r'D:', 'contract-result.txt'), np.array(pdftxt), delimiter='', fmt='%s')

    # curimg = readword.readimg(wordpath, imgdir, 'test')
    # curimg = readimg(pptxpath, imgdir, 'test')

    # r = readdxf.split_drawing_byblock(dxfpath)
    # r = readdxf.readtxt(dxfpath)
    # np.savetxt(r'D:\dwgtxt.txt', r, encoding='utf-8',fmt='%s')
    # r = readdxf.readinfo(dxfpath)

    # transtest_origin = r'D:\data\newexp-word03test.doc'
    # transtest_target = r'D:\data'
    # transdoc.doc2docx(transtest_origin, transtest_target)

    # cntarr = [1] * 5 + [3] * 3 + [11] * 4 + [12] * 6 + [13] * 48 + [14] * 24 + \
    #          [15] * 30 + [16] * 10 + [17] * 2 + [18]
    # lmin, lmax = readpdf.pdflinelen(cntarr, lenrange=4, minlen=7)
    print(r)
