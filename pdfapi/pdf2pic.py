import os
import fitz


def transpic(full_path, resultdir):
    doc = fitz.open(full_path)  # doc为Document类型，是一个包含每一页PDF文件的列表

    rotate = 0
    zoom_x = 2.0
    zoom_y = 2.0
    trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)

    # if doc.pageCount > 1:  # 获取PDF的页数
    for pg in range(doc.pageCount):
        page = doc[pg]
        pm = page.getPixmap(matrix=trans, alpha=False)  # 将其转化为光栅文件（位数）
        print(pg)
        # writePNG
        pm.writeImage(os.path.join(resultdir, str(pg) + 'page.png'))

    return doc.pageCount
