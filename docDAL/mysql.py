import os
from sqlalchemy import create_engine
import pandas as pd
import config


def get_dw_constr():
    conStr = os.environ.get("DBCONSTR")
    return conStr if conStr is not None else config.default_constr


def get_dw_engine():
    return create_engine(get_dw_constr()).connect()


def get_file_info():
    dw = get_dw_engine()
    query = '''
        SELECT * FROM file_info
    '''
    data = pd.read_sql_query(query, dw)
    return data


def clear_file_info():
    dw = get_dw_engine()
    cnt = dw.execute('truncate file_info')
    return cnt


def write_file_info(data: pd.DataFrame):
    dw = get_dw_engine()
    data.to_sql('file_info', dw, if_exists='append', index=False, method="multi")
