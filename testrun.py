import os
from docDAL import mysql as conn
import config
import pandas as pd
import core
import shutil

username = config.test_username
rawfiledir = os.path.join(config.root_dir, username, 'raw')
filedir = os.path.join(config.root_dir, username, 'f')
fname_arr = os.listdir(rawfiledir)
transname_arr = os.listdir(filedir)
transname_arr_noext = list(map(lambda x: os.path.splitext(x)[0], transname_arr))

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
    for indx, fullname in enumerate(fname_arr):
        print(fullname)
        ext_tuple = os.path.splitext(fullname)
        fname = ext_tuple[0]
        extname = ext_tuple[1]
        fpath = os.path.join(filedir, fullname)
        kwords, kwfreq = core.analysis(fpath, extname)
        result.append({'id': indx + 100, 'fname': fname, 'extname': extname, 'username': username,
                       'keywords': str(kwords), 'kwfreq': kwfreq})

    resultdf = pd.DataFrame(result)
    cnt = conn.clear_file_info()
    conn.write_file_info(resultdf)
    print('del', str(cnt), 'write', str(len(resultdf)))

# load from db
fobjs = conn.get_file_info(returnobj=True)

# print('cluster')
# cluster_result = core.file_cluster(fobjs)
# print(cluster_result)

print('classify')
core.file_classify_demo(fobjs)
