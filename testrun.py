import os
from docDAL import mysql as conn
import config
import pandas as pd
import core

username = config.test_username
rawfiledir = os.path.join(config.root_dir, username, 'raw')
fname_arr = os.listdir(rawfiledir)

result = []
for indx, fullname in enumerate(fname_arr):
    ext_tuple = os.path.splitext(fullname)
    fname = ext_tuple[0]
    extname = ext_tuple[1]
    fpath = os.path.join(rawfiledir, fullname)
    kwords, kwfreq = core.analysis(fpath, extname)
    result.append({'id': indx + 100, 'fname': fname, 'extname': extname, 'username': username,
                   'keywords': str(kwords), 'kwfreq': kwfreq})

resultdf = pd.DataFrame(result)
cnt = conn.clear_file_info()
conn.write_file_info(resultdf)
print('del', str(cnt), 'write', str(len(resultdf)))
