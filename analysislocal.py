import pandas as pd
from cloudservice import get_documenttask, download_doc
from cloudservice import get_doctag, create_doctag, delete_doctag
from cloudservice import create_doctagrel, delete_doctagrel
from cloudservice import change_step
from cloudservice import get_docs_byid, fill_docinfo
from cloudservice import get_all_projs
import time, os, shutil
import config
import core
import utils
from datetime import datetime
from wordapi import transdoc
from pptapi import transppt


def analysis_log(info, info_obj):
    print(info, info_obj)


def on_loop(project_id):
    docresponse = get_documenttask(projid=project_id)
    docdata = pd.DataFrame(docresponse)

    if len(docdata) == 0:
        return

    docdata = docdata[docdata['step'] == 1]

    docdata = (docdata
               # .sort_values('name')
               .dropna(subset=['fileUrl', 'step'])
               .reset_index()
               )

    # basepath = os.path.join(config.root_dir, str(project_id))
    basepath = r'E:\file-local-analysis'
    for indx, dt in docdata.iterrows():
        info_log_obj = {'id': dt['fileId'], 'name': dt['name']}
        analysis_log('开始', info_log_obj)

        # if not dt['fileUrl'].startswith('http'):
        #     analysis_log('无文件', info_log_obj)
        #     continue

        try:
            # 下载文件到本地文件夹
            # curpath = os.path.join(basepath, dt['name'])
            curpath = dt['fileUrl']

            # transformed = core.transform(curpath, basepath, extname)
            ext_tuple = os.path.splitext(dt['name'])
            extname = ext_tuple[1]

            # 补写
            if extname != '.dwg' and extname != '.rar':
                continue
            # 补写

            if extname == '.doc':
                transdoc.doc2docx(curpath, basepath, remove=False)
                curpath = os.path.join(basepath, dt['name'])
            if extname == '.ppt':
                transppt.ppt2pptx(curpath, basepath, remove=False)
                curpath = os.path.join(basepath, dt['name'])

            if extname == '.dwg':
                shutil.copy(curpath, basepath)
                curpath = os.path.join(basepath, dt['name'])

            if extname == '.rar':
                shutil.copy(curpath, basepath)
                curpath = os.path.join(basepath, dt['name'])

            # 很大的
            if os.path.getsize(curpath) > 50 * 1000 * 1000:
                analysis_log('文件过大', info_log_obj)
                continue
        except:
            analysis_log('下载和转换文件', info_log_obj)
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
        except Exception as e:
            analysis_log('分析成字段', info_log_obj)
            print(e)
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
    # allproj = get_all_projs()
    # if len(allproj) == 0:
    #     return []
    # projs = pd.DataFrame(allproj)['id']
    #
    # if len(projs) == 0:
    #     return []
    #
    # return sorted(set(projs), reverse=True)
    return [434]


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
    projects = find_needed_project_ids()

    loop_id = 0
    while True:
        if exitq():
            print('exit')
            print(datetime.now())
            break
        loop_id += 1
        print('loop: ' + str(loop_id))
        for pid in projects:
            time.sleep(0.1)
            on_loop(project_id=pid)
            print('loop: ' + str(loop_id) + ' / proj: ' + str(pid))
        time.sleep(2)
