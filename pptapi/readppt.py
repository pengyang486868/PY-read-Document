import os
from pptx import Presentation


def readtxt(path):
    content = []
    ppt = Presentation(path)

    for slide in ppt.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                pass
            else:
                content.append(shape.text)

    # content = '\n'.join(content)
    return content


def readimg(path, savedir, save_prefix=''):
    ppt = Presentation(path)
    imgnum = 0
    imginfo = []

    for indx, slide in enumerate(ppt.slides):
        for shape in slide.shapes:
            if hasattr(shape, 'image'):
                imgnum += 1
                fname = save_prefix + '-' + str(indx) + '-' + str(imgnum) + '-' + shape.image.filename

                # info
                imginfo.append({'fname': fname, 'keywords': 'kw,kw', 'relatedtxt': 'related'})

                # save
                with open(os.path.join(savedir, fname), 'wb') as f:
                    f.write(shape.image.blob)
                    f.close()

    return imginfo


# not in use, for experiment
def readpptx(path, resultdir):
    content = []
    ppt = Presentation(path)
    imgnum = 0

    for slide in ppt.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                if hasattr(shape, 'image'):
                    imgnum += 1
                    with open(os.path.join(resultdir, str(imgnum) + '-' + shape.image.filename), 'wb') as f:
                        f.write(shape.image.blob)
                        f.close()
            else:
                content.append(shape.text)

    content = '\n'.join(content)
    with open(os.path.join(resultdir, 'text.txt'), 'w') as f:
        f.write(content)
        f.close()
    return content
