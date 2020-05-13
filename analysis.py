import pandas as pd
from cloudservice import get_documenttask, download_doc
from cloudservice import get_doctag, create_doctag, delete_doctag
from cloudservice import create_doctagrel, delete_doctagrel
from cloudservice import change_step
import time, os
import config
import core


def test():
    docresponse = get_documenttask(projid=4)
    docdata = pd.DataFrame(docresponse)

    docdata = (docdata.sort_values('name')
               .dropna(subset=['fileUrl', 'step'])
               .reset_index()
               )

    utest = docdata['fileUrl'].tolist()[0]
    dname = docdata['name'].tolist()[0]
    # download_doc(utest, 'D:\\' + dname)

    r1 = create_doctag('混凝土', projid=4)
    r2 = create_doctag('施工', projid=4)
    # r = delete_doctag(1)
    # allt = get_doctag()
    create_doctagrel([(155, r1), (155, r2)], projid=4)
    print()


def servicetest():
    docresponse = get_documenttask(projid=4)
    docdata = pd.DataFrame(docresponse)
    # data1 = docresponse[66]
    for indx, dt in docdata.iterrows():
        dt['step'] = 1
        change_step(dt['id'], dt.to_dict(), projid=4)


def reset_steps():
    docresponse = get_documenttask(projid=4)
    docdata = pd.DataFrame(docresponse)
    for indx, dt in docdata.iterrows():
        dt['step'] = 1
        change_step(dt['id'], dt.to_dict(), projid=4)


def on_loop(project_id):
    docresponse = get_documenttask(projid=project_id)
    docdata = pd.DataFrame(docresponse)
    docdata = docdata[docdata['step'] == 1]

    docdata = (docdata.sort_values('name')
               .dropna(subset=['fileUrl', 'step'])
               .reset_index()
               )

    basepath = os.path.join(config.root_dir, str(project_id))
    for indx, dt in docdata.iterrows():
        # 下载文件到本地文件夹
        curpath = os.path.join(basepath, dt['name'])
        download_doc(dt['fileUrl'], curpath)

        # 转换文件
        ext_tuple = os.path.splitext(dt['name'])
        fname = ext_tuple[0]
        extname = ext_tuple[1]
        transformed = core.transform(curpath, basepath, extname)

        # 分析成字段
        kwords, kwfreq, pharr, nwarr, sumarr, curimg, curdrawing = core.analysis(curpath, extname, imgdir=None)

        # 文件表写入字段

        # 创建新标签并关联
        alltags = get_doctag()
        curtags = kwords.split(',')[:5]
        dtrels = []
        for curtag in curtags:
            existq = False
            for t in alltags:
                if t['name'] == curtag:
                    dtrels.append((dt['id'], t['id']))
                    existq = True
                    break
            if not existq:
                tagid = create_doctag(curtag, projid=project_id)
                dtrels.append((dt['id'], tagid))

        # 写入关联文件和标签
        create_doctagrel(dtrels, projid=project_id)

        # 更改task的阶段为已完成
        dt['step'] = 2
        change_step(dt['id'], dt.to_dict(), projid=4)

    # delete_doctagrel(13, projid=project_id)
    print()


if __name__ == '__main__':
    for _ in range(1):
        on_loop(project_id=4)
        time.sleep(5)
