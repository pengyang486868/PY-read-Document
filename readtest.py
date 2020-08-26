from pptapi.readppt import readpptx, readimg, readnotes
from pdfapi.pdf2pic import transpic
from pdfapi import readpdf
from dwgapi import readdxf
from wordapi import readword, transdoc
from rarapi import readrar
import numpy as np

import os
import config
import uuid

if __name__ == '__main__':
    pptxpath = r'D:\qqsave\854525261\FileRecv\新员工培训之《方案管理》.pptx'
    # pptxpath = r'D:\filedata\uname\f/C-technical-05+第二节-混凝土灌注桩施工.pptx'
    pdfpath = r'E:\contract.pdf'
    # pdfpath = r'D:/filedata/uname\f\M-bimsys-11+广联达BIM体系.pdf'
    pdftxtpath = r'D:/data/pdftxt.pdf'

    # dxfpath = r'D:\filedata\uname\dwg/D-commercial-01+来福士T2-min.dxf'
    dxfpath = r'D:\filedata\uname\儿童医院电气-min.dxf'

    wordpath = r'E:\file-local-analysis\室外总体施工方案A.docx'

    zippath = r'F:\402\001 交响乐团20130311需合并\施工方案\交响乐团方案\交响乐团方案2.zip'
    rarpath = r'F:\402\001 交响乐团20130311需合并\施工方案\排演厅双层板墙模板.rar'

    resultdir = r'D:/result'

    username = config.test_username
    imgdir = os.path.join(config.root_dir, 'images')
    r = readimg(pptxpath, imgdir, str(uuid.uuid4()))
    # r = readword.readimg(wordpath, imgdir, str(uuid.uuid4()))
    print(r)

    # r = readimg(pptxpath, resultdir, save_prefix='XXB-')
    # r = readnotes(pptxpath)

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

    # transtest_origin = r'D:\施工组织设计15.doc'
    # transtest_target = r'D:\data'
    # transdoc.doc2docx(transtest_origin, transtest_target)

    # cntarr = [1] * 5 + [3] * 3 + [11] * 4 + [12] * 6 + [13] * 48 + [14] * 24 + \
    #          [15] * 30 + [16] * 10 + [17] * 2 + [18]
    # lmin, lmax = readpdf.pdflinelen(cntarr, lenrange=4, minlen=7)

    # r1 = readrar.readzip(zippath, rm_prefix=True, maxnames=5)
    # r2 = readrar.readrar(rarpath, rm_prefix=True)
    # print(r1)
    # print(r2)
