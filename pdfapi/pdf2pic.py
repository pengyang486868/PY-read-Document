import os
import fitz


def topic(full_path, resultdir):
    # base_path = input("请输入要转换的文件路径：")  # 输入要转换的PDF所在的文件夹
    # filenames = os.listdir(base_path)  # 获取PDF文件列表
    # for filename in filenames:
    # full_path = os.path.join(base_path, filename)  # 拼接，得到PDF文件的绝对路径
    print(full_path)
    doc = fitz.open(full_path)  # 打开一个PDF文件，doc为Document类型，是一个包含每一页PDF文件的列表
    rotate = 0  # 设置图片的旋转角度
    zoom_x = 2.0  # 设置图片相对于PDF文件在X轴上的缩放比例
    zoom_y = 2.0  # 设置图片相对于PDF文件在Y轴上的缩放比例
    trans = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)

    # if doc.pageCount > 1:  # 获取PDF的页数
    for pg in range(doc.pageCount):
        page = doc[pg]  # 获得第pg页
        pm = page.getPixmap(matrix=trans, alpha=False)  # 将其转化为光栅文件（位数）
        # new_full_name = full_path.split(".")[0]  # 保证输出的文件名不变
        print(pg)
        pm.writeImage(os.path.join(resultdir, str(pg) + 'page.png'))
        # 我本来想输出为jpg文件，但是在网页中都是png格式（即调用writePNG），再转换成别的图像文件前，最好查一下是否支持
    return doc.pageCount
