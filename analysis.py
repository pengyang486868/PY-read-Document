import pandas as pd
from cloudservice import get_documenttask, download_doc
from cloudservice import get_doctag, create_doctag, delete_doctag
from cloudservice import create_doctagrel, delete_doctagrel
from cloudservice import change_step
from cloudservice import get_docs_byid, fill_docinfo
from cloudservice import get_all_projs, get_file_projs
import time, os
import config
import core
import utils
from datetime import datetime


def analysis_log(info, info_obj):
    print(info, info_obj)


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
    # docresponse = get_documenttask(projid=4)
    # docdata = pd.DataFrame(docresponse)
    # # data1 = docresponse[66]
    # for indx, dt in docdata.iterrows():
    #     dt['step'] = 1
    #     change_step(dt['id'], dt.to_dict(), projid=4)
    doc1 = get_docs_byid(153, projid=4)
    # doc1 = docs_response[10]
    doc1['abstract'] = 'new abstract'
    updated = {
        "name": doc1['name'],
        "remark": doc1['remark'],
        "keyWord": doc1['keyWord'],
        "abstract": doc1['abstract'],
        "url": doc1['url'],
        "fileSize": doc1['fileSize'],
        "fileType": doc1['fileType'],
        "directoryId": doc1['directoryId'],
        "creatorId": 1,
        "uploaderId": 1,
        "newWords": "string",
        "wordFrequency": "string",
        "phrases": "string"
    }
    fill_docinfo(doc1['id'], updated, projid=4)


def reset_steps():
    docresponse = get_documenttask(projid=4)
    docdata = pd.DataFrame(docresponse)
    for indx, dt in docdata.iterrows():
        dt['step'] = 1
        change_step(dt['id'], dt.to_dict(), projid=4)


def on_loop(project_id):
    docresponse = get_documenttask(projid=project_id)
    docdata = pd.DataFrame(docresponse)
    if len(docdata) == 0:
        return

    docdata = docdata[docdata['step'] == 1]
    docdata = docdata.tail(config.n_for_project_in_loop)

    docdata = (docdata.sort_values('name')
               .dropna(subset=['fileUrl', 'step'])
               .reset_index()
               )

    # basepath = os.path.join(config.root_dir, str(project_id))
    basepath = config.root_dir
    for indx, dt in docdata.iterrows():
        info_log_obj = {'id': dt['fileId'], 'name': dt['name']}
        # analysis_log('开始', info_log_obj)
        if not dt['fileUrl'].startswith('http'):
            analysis_log('无文件', info_log_obj)
            continue

        try:
            # 下载文件到本地文件夹
            curpath = os.path.join(basepath, dt['name'])
            download_doc(dt['fileUrl'], curpath)
        except:
            analysis_log('下载文件', info_log_obj)
            continue

        # 转换文件
        try:
            # 很大的
            if os.path.getsize(curpath) > 100 * 1000 * 1000:
                analysis_log('文件过大', info_log_obj)
                dt['step'] = 4
                change_step(dt['id'], dt.to_dict(), projid=project_id)
                analysis_log('完成', info_log_obj)
                continue

            ext_tuple = os.path.splitext(dt['name'])
            fname = ext_tuple[0]
            extname = ext_tuple[1]
            transformed = core.transform(curpath, basepath, extname)
        except:
            analysis_log('转换文件', info_log_obj)
            continue

        # 分析成字段
        try:
            kwords, kwfreq, pharr, nwarr, sumarr, *img_none = core.analysis(
                curpath, extname, imgdir=None, do_drawings=True)

            kwords_arr = kwords.split(',')
            real_kwords = []
            for kw in kwords_arr:
                if is_real_kw(kw):
                    real_kwords.append(kw)
            if len(real_kwords) > 5:
                low_kw = real_kwords[5:]
            else:
                low_kw = []
        except:
            analysis_log('分析成字段', info_log_obj)
            continue

        # 文件表写入字段
        file_table_write_success = False
        try:
            doc_record = get_docs_byid(dt['fileId'], projid=project_id)

            # choose summary
            real_summary = []
            for su in sumarr:
                if is_real_summary(su):
                    real_summary.append(su)
            summarylimit = 3
            if len(real_summary) > summarylimit:
                real_summary = sorted(real_summary, key=lambda x: len(x), reverse=True)[:summarylimit]

            nwlimit = 900
            nwarr = utils.remove_blank(nwarr)
            if len(nwarr) > nwlimit:
                nwarr = nwarr[:nwlimit]
            updated = {
                # "keyWord": kwords,
                "keyWord": ','.join(low_kw),
                "abstract": ','.join(real_summary),
                "newWords": nwarr,
                "wordFrequency": kwfreq,
                "phrases": pharr
            }

            doc_record.update(updated)
            # print(doc_record)
            fill_docinfo(doc_record['id'], doc_record, projid=project_id)
            file_table_write_success = True
        except Exception as e:
            analysis_log('文件表填入', info_log_obj)
            continue

        # 创建新标签并关联
        try:
            if not real_kwords:
                analysis_log('无内容', info_log_obj)
            else:
                alltags = get_doctag(projid=project_id)
                if len(real_kwords) >= config.web_keywords_num:
                    curtags = real_kwords[:config.web_keywords_num]
                else:
                    curtags = real_kwords
                dtrels = []
                for curtag in curtags:
                    existq = False
                    for t in alltags:
                        if str(t['name']).upper() == str(curtag).upper():
                            dtrels.append((dt['fileId'], t['id']))
                            existq = True
                            break
                    if not existq:
                        tagid = create_doctag(curtag, projid=project_id)
                        dtrels.append((dt['fileId'], tagid))
                # 写入关联文件和标签
                create_doctagrel(dtrels, projid=project_id)
        except:
            analysis_log('标签', info_log_obj)
            continue

        # 更改task的阶段为已完成
        if file_table_write_success:
            dt['step'] = 2
            change_step(dt['id'], dt.to_dict(), projid=project_id)

        # 删除本地下载文件
        pass
        analysis_log('完成', info_log_obj)

    # delete_doctagrel(13, projid=project_id)
    print('end proj')


def is_real_kw(kw: str) -> bool:
    if len(kw) < 2:
        return False

    undercount = 0
    for c in kw:
        if c == '_':
            undercount += 1
    if undercount / len(kw) > 0.499:
        return False
    return True


def is_real_summary(su) -> bool:
    if len(su) < 6:
        return False
    return True


def find_needed_project_ids():
    # docresponse = get_documenttask(projid=0)
    allproj = get_all_projs()
    if len(allproj) == 0:
        return []
    projs = pd.DataFrame(allproj)['id'].tolist()

    if len(projs) == 0:
        return []

    return sorted(set([p for p in projs if p not in config.exclude_projects]), reverse=True)


def exitq() -> bool:
    with open('stop.cms') as sf:
        sign = sf.readline()
    sign = int(sign)
    if sign > 0:
        return True
    return False


if __name__ == '__main__':
    # servicetest()
    # projects = config.analyzing_projects
    projects = find_needed_project_ids()  # with exclude
    have_file_projects = get_file_projs()

    loop_id = 0
    while True:
        if exitq():
            print('exit')
            print(datetime.now())
            break
        loop_id += 1
        print('loop: ' + str(loop_id))
        for pid in projects:
            if pid not in have_file_projects:
                continue
            time.sleep(0.1)
            on_loop(project_id=pid)
            print('loop: ' + str(loop_id) + ' / proj: ' + str(pid))
        time.sleep(2)
