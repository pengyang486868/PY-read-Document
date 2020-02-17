from docx import Document
import os


def readimg(full_path, resultdir):
    doc = Document(full_path)
    doc_part = doc.part
    count = 0
    for ishape in doc.inline_shapes:
        blip = ishape._inline.graphic.graphicData.pic.blipFill.blip
        rID = blip.embed
        image_part = doc_part.related_parts[rID]

        fr = open(os.path.join(resultdir, rID + '.png'), "wb")
        fr.write(image_part._blob)
        fr.close()
        count += 1
    return count
