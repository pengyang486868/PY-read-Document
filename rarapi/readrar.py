import rarfile
import zipfile
import os, re
from typing import List


def readrar(fpath, rm_prefix=False, maxnames=10):
    rar_file = rarfile.RarFile(fpath, mode='r')  # mode的值只能为'r'
    rar_list: List[str] = rar_file.namelist()  # 得到压缩包里所有的文件

    # for f in rf_list:
    #     rf.extract(f, folder_abs)  # 循环解压，将文件解压到指定路径
    # 一次性解压所有文件到指定目录
    # rf.extractall(path) # 不传path，默认为当前目录

    # 去掉压缩包名和斜杠
    if rm_prefix:
        packname_pattern = re.compile('^' + getpackname(fpath))
        rar_list = [re.sub(r'^/', '', re.sub(packname_pattern, '', x)) for x in rar_list]

    rar_file.close()
    return sorted([x for x in rar_list if len(x) > 0], key=len, reverse=False)[:maxnames]  # 短的在前面


def readzip(fpath, rm_prefix=False, maxnames=10):
    # 基本格式：zipfile.ZipFile(filename[,mode[,compression[,allowZip64]]])
    # mode：可选 r,w,a 代表不同的打开文件的方式；r 只读；w 重写；a 添加
    # compression：指出这个 zipfile 用什么压缩方法，默认是 ZIP_STORED，另一种选择是 ZIP_DEFLATED；
    # allowZip64：bool型变量，当设置为True时可以创建大于 2G 的 zip 文件，默认值 True

    zip_file = zipfile.ZipFile(fpath)
    zip_list = zip_file.namelist()

    # 解决中文乱码
    decoded_zip_list = []
    for name in zip_list:
        try:
            decoded_zip_list.append(name.encode('cp437').decode('gbk'))
        except:
            try:
                decoded_zip_list.append(name.encode('utf-8').decode('utf-8'))
            except:
                pass

    # for f in zip_list:
    #     zip_file.extract(f, folder_abs)  # 循环解压文件到指定目录

    # 去掉压缩包名和斜杠
    if rm_prefix:
        packname_pattern = re.compile('^' + getpackname(fpath))
        decoded_zip_list = [re.sub(r'^/', '', re.sub(packname_pattern, '', x)) for x in decoded_zip_list]

    zip_file.close()
    return sorted([x for x in decoded_zip_list if len(x) > 0], key=len, reverse=False)[:maxnames]


# name of archive without extname
def getpackname(p):
    purename = os.path.splitext(os.path.basename(p))[0]
    return purename
