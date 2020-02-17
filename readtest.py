from pptapi.readppt import readpptx
from pdfapi.pdf2pic import transpic
from pdfapi import readpdf
from dwgapi import readdxf
from wordapi import readword, transdoc

if __name__ == '__main__':
    pptxpath = r'D:/2020增补-2019彭阳年终.pptx'
    pdfpath = r'D:/data/pdftest.pdf'
    pdftxtpath = r'D:/data/pdftxt.pdf'
    dxfpath = r'D:/data/dxftest.dxf'
    wordpath = r'D:/data/wordtxt.docx'
    resultdir = r'D:/result'

    # txt = readppt.readpptx(pptxpath, resultdir)
    # pagecount = transpic(pdfpath, resultdir)
    # readdxf.read(dxfpath)
    # tarr = readpdf.readtext(pdftxtpath)
    # print(tarr)

    word03path = r'D:/data/word03test.doc'
    success, newfile = transdoc.doc2docx(word03path)
    if success:
        # cnt = readword.readimg(newfile, resultdir)
        doctxt = readword.readtxt(newfile)
        print(doctxt)
