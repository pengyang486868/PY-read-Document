import pandas as pd
from cloudservice import get_documenttask, download_doc, get_new_doc_task_db
from cloudservice import get_doctag, create_doctag, delete_doctag
from cloudservice import create_doctagrel, delete_doctagrel
from cloudservice import change_step
from cloudservice import get_docs_byid, fill_docinfo
from cloudservice import get_all_projs, get_file_projs
from cloudservice import add_attachment
import time, os
import config
import core
import utils
from datetime import datetime


def analysis_log(info, info_obj):
    print(info, info_obj)


def on_loop(project_id):
    # docresponse = get_documenttask(projid=project_id)
    # docdata = pd.DataFrame(docresponse)
    docdata = get_new_doc_task_db(project_id, 'dwg')
    if len(docdata) == 0:
        return

    # docdata = docdata[(docdata['step'] == 1) & (docdata['fileType'] == 'dwg')]
    docdata = docdata.tail(config.n_for_project_in_loop)
    docdata.columns = [s[0].lower() + s[1:] for s in docdata.columns]

    docdata = (docdata.dropna(subset=['fileUrl', 'step'])
               .reset_index()
               )

    # docdata = (docdata.sort_values('name')
    #            .dropna(subset=['fileUrl', 'step'])
    #            .reset_index()
    #            )

    # basepath = os.path.join(config.root_dir, str(project_id))
    basepath = config.root_dir
    imgdir = os.path.join(config.root_dir, 'images')
    for indx, dt in docdata.iterrows():
        dt['createTime'] = str(dt['createTime'].asm8)
        print(datetime.now())
        info_log_obj = {'id': dt['fileId'], 'name': dt['name']}
        # analysis_log('开始', info_log_obj)
        if not dt['fileUrl'].startswith('http'):
            dt['step'] = 6
            change_step(dt['id'], dt.to_dict(), projid=project_id)
            analysis_log('无文件', info_log_obj)
            continue

        # 不分析一些类型
        no_analysis = False
        for tp in config.skip_file_types:
            if not dt['fileType'] or tp in dt['fileType']:
                dt['step'] = 5
                change_step(dt['id'], dt.to_dict(), projid=project_id)
                info_log_obj['type'] = dt['fileType']
                analysis_log('跳过类型', info_log_obj)
                no_analysis = True
                break
        if no_analysis:
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
            if os.path.getsize(curpath) > 300 * 1000 * 1000:
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
            kwords, kwfreq, pharr, nwarr, sumarr, attaimges, *drawing_none = core.analysis(
                curpath, extname, imgdir=imgdir, do_drawings=True)

            kwords_arr = kwords.split(',')
            real_kwords = []
            for kw in kwords_arr:
                if is_real_kw(kw):
                    real_kwords.append(kw)
            if len(real_kwords) > 5:
                low_kw = real_kwords[5:]
            else:
                low_kw = []
        except Exception as e:
            dt['step'] = 7
            change_step(dt['id'], dt.to_dict(), projid=project_id)
            analysis_log('分析成字段', info_log_obj)
            print(e)
            continue

        # 图片附件
        try:
            # 上传oss
            upload_result = core.upload_images(attaimges)

            # 写入附件表
            for atta in upload_result:
                atta_obj = {
                    "name": atta['name'],
                    "remark": "",
                    "keyword": "",
                    "abstract": utils.remove_blank(atta['abstract']),
                    "url": atta['url'],
                    "fileSize": atta['fileSize'],
                    "fileType": atta['fileType'],
                    "newWords": "",
                    "wordFrequency": "",
                    "phrases": "",
                    "linkType": "文件关联图片",
                    "fileId": dt['fileId']
                }
                add_attachment(atta_obj, projid=project_id)
        except Exception as e:
            print(e)
            analysis_log('图片附件', info_log_obj)
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
            print(e)
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
        except Exception as e:
            analysis_log('标签', info_log_obj)
            print(e)
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
    # print(sign)
    if sign > 0:
        return True
    return False


if __name__ == '__main__':
    # servicetest()
    # projects = find_needed_project_ids()  # with exclude
    projects = [687]
    # projects = [26, 193, 406, 53]
    have_file_projects = projects
    # have_file_projects = get_file_projs()

    loop_id = 0
    while True:
        if exitq():
            print('exit')
            print(datetime.now())
            break
        loop_id += 1
        print('loop: ' + str(loop_id))
        for pid in projects:
            try:
                print('loop: ' + str(loop_id) + ' / proj: ' + str(pid))
                if pid not in have_file_projects:
                    continue
                time.sleep(0.1)
                on_loop(project_id=pid)
                print()
            except Exception as e:
                print(e)

        time.sleep(2)
