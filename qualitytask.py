from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re, json
from snownlp import SnowNLP
from cloudservice import post_action

conStr = "mysql+pymysql://yufq007:shsijian007@rdsira6v2ira6v2public.mysql.rds.aliyuncs.com:3307/njg60"


# data
def get_data():
    dw = create_engine(conStr).connect()
    query = '''SELECT t.id,t.number,t.`describe`,c.category,u.`name` AS major
                FROM taskandflow_projectevent AS t
                LEFT JOIN taskandflow_eventcategory AS c ON c.id=t.category_id
                LEFT JOIN emscc4.userandprj_usermajor AS u ON u.id=t.major_id
                WHERE t.number NOT LIKE 'CLYS%%' '''
    data = pd.read_sql_query(query, dw)
    return data


def remove_nums(s):
    pattern = r'[A-Za-z0-9_\-\.\(\)\#、，。/]+'
    s = re.sub(pattern, ' ', s)
    s = s.rstrip().lstrip()
    return s


def makedic(data: pd.DataFrame):
    result = {}
    for indx, row in data.iterrows():
        cate = row['category']
        major = row['major']
        sobj = SnowNLP(remove_nums(row['describe']))
        words = sobj.words

        for w in words:
            # keyword record
            if w not in result:
                result[w] = {'cate': {}, 'major': {}}

            # add cate score
            if cate is not None:
                if cate not in result[w]['cate']:
                    result[w]['cate'][cate] = 0
                result[w]['cate'][cate] += 1

            # add major score
            if major is not None:
                if major not in result[w]['major']:
                    result[w]['major'][major] = 0
                result[w]['major'][major] += 1

    return result


if __name__ == '__main__':
    d = get_data()  # .head(20)
    analysis_dic = makedic(d)
    with open(r'./quality.json', 'w') as f:
        json.dump(analysis_dic, f)
