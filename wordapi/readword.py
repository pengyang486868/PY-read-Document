from docx import Document
import os
import re


def readtxt(full_path):
    doc = Document(full_path)
    result = []
    for para in doc.paragraphs:
        result.append(para.text)
    # # 表格
    # tbs = doc.tables
    # for tb in tbs:
    #     for row in tb.rows:
    #         for cell in row.cells:
    #             print(cell.text)
    #             # or
    #             '''text = ''
    #             for p in cell.paragraphs:
    #                 text += p.text
    #             print(text)'''
    return result


def readimg(full_path, savedir, save_prefix=''):
    doc = Document(full_path)
    doc_part = doc.part
    imgcount = 0

    # delete empty paragraphs
    notemptyp = []
    for p in doc.paragraphs:
        xmlstr = p._p.xml
        if 'graphicData' in xmlstr or len(p.text) > 0:
            notemptyp.append(p)

    contextdic = {}
    for indx, p in enumerate(notemptyp):
        xmlstr = p._p.xml
        if not 'graphicData' in xmlstr:
            continue

        # r:embed="rId5"
        ridreg = re.compile(r'r:embed="(.*)"')
        cur_rids = ridreg.findall(xmlstr)
        if len(cur_rids) < 1:
            continue
        if indx < 1 or doc.paragraphs[indx + 1].text.startswith('图'):
            contextdic[cur_rids[0]] = doc.paragraphs[indx + 1].text
        else:
            contextdic[cur_rids[0]] = doc.paragraphs[indx - 1].text

    imginfo = []
    for ishape in doc.inline_shapes:
        imgcount += 1
        blip = ishape._inline.graphic.graphicData.pic.blipFill.blip
        rID = blip.embed
        image_part = doc_part.related_parts[rID]

        # save
        fname = save_prefix + '-' + str(imgcount) + '-' + rID + '.png'
        fr = open(os.path.join(savedir, fname), "wb")
        fr.write(image_part._blob)
        fr.close()

        # find related text
        imginfo.append({'fname': fname,
                        'relatedtxt': contextdic[rID] if rID in contextdic else ''})

    return imginfo
