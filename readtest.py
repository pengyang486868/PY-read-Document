from pptapi.readppt import readpptx
from pdfapi.pdf2pic import transpic

if __name__ == '__main__':
    pptxpath = r'D:/2020增补-2019彭阳年终.pptx'
    pdfpath = r'D:/data/pdftest.pdf'
    resultdir = r'D:/result'

    # txt = readppt.readpptx(pptxpath, resultdir)
    pagecount = p2p.transpic(pdfpath, resultdir)
