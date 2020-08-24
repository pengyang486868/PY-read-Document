import os
from cloudservice import add_file, add_dir, get_dir_subs, get_root_dir_id
from pathlib import Path
import pandas as pd


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
    r = add_file(fdata, projid)
    return r


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
            try:
                uploadfile(str(thing), rootid, projid)
                print('upload ' + str(thing))
            except:
                try:
                    print('failed ' + str(thing))
                except:
                    print('solid failed')


# if exist return id, if not exist create it then return id
def get_dirid(p, curdirid, projid):
    subs = get_dir_subs(curdirid, projid)
    for sd in subs:
        if sd['name'] == p.split('\\')[-1]:
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
    pass
    # do_batch_upload(Path(r'F:\402\004 小洋山资料备份-晓莉'), 240, 42)
    # do_batch_upload(Path(r'F:\402\testupload'), 36, 200)
    # do_batch_upload(Path(r'F:\402\001 交响乐团20130311需合并'), 434, 202)
    # do_batch_upload(Path(r'F:\dfyyfile\东方医院'), projid=230, rootid=2211)
    # do_batch_upload(Path(r'D:\技术群文档'), projid=687, rootid=2370)
    # http:\\10.6.0.50:6789\files\工程资料 01\01 工程资料\404\008 解放日报-张雷\1.txt
    # do_batch_upload(Path(r'\\192.168.11.70\工程资料 02\03 工程资料\404\国金资料'), projid=183, rootid=4000)
    # uploadfile(r'E:\work\论文\空调故障诊断与风险评估.pdf',projid=33,dirid=38292)
    # proj_infos = [['401', '001 中国馆', 196]]
    # proj_infos = pd.read_csv(r'.\projs.csv')
    # for indx, info in proj_infos.iterrows():
    #     subdir = str(info['sub'])
    #     projname = info['name']
    #     projid = info['pid']
    #
    #     pathstr = os.path.join(r'\\192.168.11.70\工程资料 01\01 工程资料', subdir, projname)
    #     test = Path(pathstr)
    #
    #     try:
    #         add_dir(projname, None, projid)
    #     except:
    #         pass
    #     rootid = get_root_dir_id(projid)
    #
    #     do_batch_upload(Path(pathstr), projid=projid, rootid=rootid)
