from pptapi.readppt import readpptx
from pdfapi.pdf2pic import transpic
from pdfapi import readpdf
from dwgapi import readdxf
from wordapi import readword, transdoc

if __name__ == '__main__':
    pptxpath = r'D:/2020增补-2019彭阳年终.pptx'
    pdfpath = r'D:/data/pt.pdf'
    pdftxtpath = r'D:/data/pdftxt.pdf'
    dxfpath = r'D:/data/dxftest.dxf'
    wordpath = r'D:/data/wordtxt.docx'
    resultdir = r'D:/result'

    pdftxt = readpdf.readtext(pdfpath)

    # cntarr = [1] * 5 + [3] * 3 + [11] * 4 + [12] * 6 + [13] * 48 + [14] * 24 + \
    #          [15] * 30 + [16] * 10 + [17] * 2 + [18]
    # lmin, lmax = readpdf.pdflinelen(cntarr, lenrange=4, minlen=7)
    print()
