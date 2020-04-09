import os
from docDAL import mysql as conn
import config
import pandas as pd
import core
import shutil

username = config.test_username
rawfiledir = os.path.join(config.root_dir, username, 'raw')
filedir = os.path.join(config.root_dir, username, 'f')
imgdir = os.path.join(config.root_dir, username, 'image')
fname_arr = os.listdir(rawfiledir)
transname_arr = os.listdir(filedir)
transname_arr_noext = list(map(lambda x: os.path.splitext(x)[0], transname_arr))

retransform = False
if retransform:
    print('transform')
    for fullname in fname_arr:
        print(fullname)
        ext_tuple = os.path.splitext(fullname)
        fname = ext_tuple[0]
        extname = ext_tuple[1]
        if fname not in transname_arr_noext:
            fpath = os.path.join(rawfiledir, fullname)
            transformed = core.transform(fpath, filedir, extname)
            if not transformed:
                shutil.copy(fpath, filedir)

reanalysis = False
if reanalysis:
    print('analysis')
    result = []
    imgresult = []
    drawingresult = []
    for indx, fullname in enumerate(fname_arr):
        print(fullname)
        ext_tuple = os.path.splitext(fullname)
        fname = ext_tuple[0]
        extname = ext_tuple[1]
        fpath = os.path.join(filedir, fullname)
        kwords, kwfreq, pharr, nwarr, sumarr, curimg, curdrawing = core.analysis(fpath, extname, imgdir)
        fid = indx + 100
        result.append({'id': fid, 'fname': fname, 'extname': extname, 'username': username,
                       'keywords': kwords, 'kwfreq': kwfreq,
                       'phrase': pharr, 'newwords': nwarr, 'summary': sumarr})
        imgresult += curimg
        for d in curdrawing:
            d['drawing_id'] = fid
            d['title'] = ''
        drawingresult += curdrawing

    resultdf = pd.DataFrame(result)
    imgresultdf = pd.DataFrame(imgresult)[['fname', 'keywords', 'newwords', 'relatedtxt', 'docname']]
    drawingresultdf = pd.DataFrame(drawingresult)

    cnt = conn.clear_file_info()
    conn.write_file_info(resultdf)
    conn.write_img_info(imgresultdf)
    conn.write_drawingsplit_info(drawingresultdf)
    print('del', str(cnt), 'write', str(len(resultdf)))

aiq = True
if aiq:
    # load from db
    fobjs = conn.get_file_info(returnobj=True)

    # print('cluster')
    # cluster_result = core.file_cluster(fobjs)

    print('classify')
    core.file_classify_demo(fobjs)
