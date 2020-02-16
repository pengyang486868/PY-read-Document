from pptapi.readppt import readpptx
from pdfapi.pdf2pic import transpic
from dwgapi import readdxf

if __name__ == '__main__':
    pptxpath = r'D:/2020增补-2019彭阳年终.pptx'
    pdfpath = r'D:/data/pdftest.pdf'
    dxfpath = r'D:/data/dxftest.dxf'
    resultdir = r'D:/result'

    # txt = readppt.readpptx(pptxpath, resultdir)
    # pagecount = transpic(pdfpath, resultdir)
    readdxf.read(dxfpath)
