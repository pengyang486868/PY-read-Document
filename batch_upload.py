import os
from cloudservice import add_file, add_dir, get_dir_subs
from pathlib import Path


def test():
    uploadfile(os.path.join('我文件夹', 'test1.docx'), dirid=39, projid=36)
    print()


def create_dir_test():
    add_dir('addsub', 39, 36)


def uploadfile(fpath, dirid, projid):
    # fpath = os.path.join(config.batch_file_upload_root, relative_fpath)
    fdir, fname = os.path.split(fpath)
    ftype = os.path.splitext(fname)[-1]
    fsize = os.path.getsize(fpath)
    fdata = {
        "name": fname,
        "remark": "",
        "keyWord": "",
        "abstract": "",
        "url": fpath,
        "fileSize": fsize,
        "fileType": ftype,
        "directoryId": dirid,
        "creatorId": 1,
        "uploaderId": 0,
        "newWords": "",
        "wordFrequency": "",
        "phrases": ""
    }
    add_file(fdata, projid)


def do_batch_upload(dpath: Path, projid, rootid):
    for thing in dpath.iterdir():
        # 是文件夹则递归
        if thing.is_dir():
            name = str(thing).split('\\')[-1]
            if name.startswith('__'):  # 双下划线跳过
                print('skip ' + str(thing))
                continue
            do_batch_upload(thing, projid, get_dirid(str(thing), rootid, projid))
        # 是文件则上传
        if thing.is_file():
            uploadfile(str(thing), rootid, projid)
            print('upload ' + str(thing))


# if exist return id, if not exist create it then return id
def get_dirid(p, curdirid, projid):
    subs = get_dir_subs(curdirid, projid)
    for sd in subs:
        if sd['name'] == p:
            return sd['id']

    # 如果没返回 就是没这个文件夹 创建一个
    createname = p.split('\\')[-1]
    add_dir(createname, curdirid, projid)
    print('create ' + p)

    # 再找到文件夹ID
    subs = get_dir_subs(curdirid, projid)
    for sd in subs:
        if sd['name'] == createname:
            return sd['id']
    return 0


if __name__ == '__main__':
    # do_batch_upload(Path(r'F:\402\004 小洋山资料备份-晓莉'), 240, 42)
    # do_batch_upload(Path(r'F:\402\testupload'), 36, 200)
    # do_batch_upload(Path(r'F:\402\001 交响乐团20130311需合并'), 434, 202)
    do_batch_upload(Path(r'F:\402\002 东海园文件汇备份-晓莉'), 587, 634)
