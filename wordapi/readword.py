from docx import Document
import os


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
    count = 0
    for ishape in doc.inline_shapes:
        blip = ishape._inline.graphic.graphicData.pic.blipFill.blip
        rID = blip.embed
        image_part = doc_part.related_parts[rID]

        # save
        fr = open(os.path.join(savedir, rID + '.png'), "wb")
        fr.write(image_part._blob)
        fr.close()
        count += 1
    return count
