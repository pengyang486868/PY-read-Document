import os
from sqlalchemy import create_engine
import pandas as pd
import config
from model import FileInfo, ImageInfo


def get_dw_constr():
    conStr = os.environ.get("DBCONSTR")
    return conStr if conStr is not None else config.default_constr


def get_dw_engine():
    return create_engine(get_dw_constr()).connect()


def get_file_info(returnobj=False):
    dw = get_dw_engine()
    query = '''
        SELECT * FROM file_info
    '''
    data = pd.read_sql_query(query, dw)

    if not returnobj:
        return data

    objs = []
    for indx, row in data.iterrows():
        curobj = FileInfo()
        curobj.id = row['id']
        curobj.fname = row['fname']
        curobj.extname = row['extname']
        curobj.username = row['username']
        curobj.keywords = row['keywords'].split(',')
        if row['kwfreq']:
            curobj.kwfreq = list(map(int, row['kwfreq'].split(',')))
        else:
            curobj.kwfreq = []
        curobj.phrase = row['phrase'].split(',')
        curobj.newwords = row['newwords'].split(',')
        curobj.label = row['label']
        if row['istest'] == 1:
            curobj.istest = True
        objs.append(curobj)
    return objs


def clear_file_info():
    dw = get_dw_engine()
    res = dw.execute('DELETE FROM file_info WHERE id>0')
    return res.rowcount


def write_file_info(data: pd.DataFrame):
    dw = get_dw_engine()
    data.to_sql('file_info', dw, if_exists='append', index=False, method="multi")


def get_img_info(returnobj=False):
    dw = get_dw_engine()
    query = '''
        SELECT * FROM file_image
    '''
    data = pd.read_sql_query(query, dw)

    if not returnobj:
        return data

    objs = []
    for indx, row in data.iterrows():
        curobj = ImageInfo()
        curobj.id = row['id']
        curobj.fname = row['fname']
        curobj.keywords = row['keywords'].split(',')
        curobj.newwords = row['newwords'].split(',')
        objs.append(curobj)
    return objs


def clear_img_info():
    dw = get_dw_engine()
    res = dw.execute('DELETE FROM file_image WHERE id>0')
    return res.rowcount


def write_img_info(data: pd.DataFrame):
    dw = get_dw_engine()
    data.to_sql('file_image', dw, if_exists='append', index=False, method="multi")


def write_drawingsplit_info(data: pd.DataFrame):
    dw = get_dw_engine()
    data.to_sql('file_drawingsplit', dw, if_exists='append', index=False, method="multi")
