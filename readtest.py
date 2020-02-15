from pptapi import readppt
from pdfapi import pdf2pic

if __name__ == '__main__':
    pptxpath = r'D:/2020增补-2019彭阳年终.pptx'
    pdfpath = r'D:/data/pdftest.pdf'
    resultdir = r'D:/result'

    # txt = readppt.readpptx(pptxpath, resultdir)
    pagecount = pdf2pic.topic(pdfpath, resultdir)

    # print(txt)
