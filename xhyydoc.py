import re, os
from collections import Counter
from kafka import KafkaProducer
import time, json
from datetime import datetime
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from snownlp import SnowNLP

fname = 'xhyy-file-names.txt'
fkw = 'xhyy-file-keywords.txt'
fkw_final = 'xhyy-file-keywords-final.txt'


def get_data(lastid=-1, limit=100):
    constr = "mysql+pymysql://scg4:zhjzydsjptyjzx@180.167.191.174:3306/dfyyfm512"
    conn = create_engine(constr).connect()
    query = '''SELECT d.id,d.`name`,d.filepath,d.filesize,u.truename,d.createtime,d.filetype
                FROM filemanage_document AS d
                LEFT JOIN usermanagement_user_profile AS u
                ON u.id=d.creator_id
                WHERE d.id>{} ORDER BY d.id LIMIT {}
                '''.format(lastid, limit)

    return pd.read_sql_query(query, conn)


# 一次性提取中文
def save_names():
    data = get_data(-1)  # .head(20)
    names = data['name'].tolist()

    pattern = r'[A-Za-z0-9_\-\.\(\)]*'
    names = [re.sub(pattern, '', x) for x in names]
    names = [x.rstrip().lstrip() for x in names if x and len(x) > 2]

    with open(fname, 'w', encoding='utf-8') as f:
        for n in names:
            f.write(n)
            f.write('\n')


# 一次性计算标签
def calculate_labels():
    with open(fname, 'r', encoding='utf-8') as f:
        names = f.readlines()

    kw = []
    for n in names:
        sobj = SnowNLP(n)
        kw += [x for x in sobj.keywords(limit=3) if len(x) > 1]

    keywords = [x[0] for x in Counter(kw).most_common(30)]

    with open(fkw, 'w', encoding='utf-8') as f:
        for n in keywords:
            f.write(n)
            f.write('\n')


# 最终label
def get_final_labels():
    with open(fkw_final, 'r', encoding='utf-8') as f:
        kws = f.read()
    return kws.split()


# 从头计算写入
def recalculate():
    labels = get_final_labels()

    last_id_db = -1
    # last_id_db = 19605
    while True:
        print('last ', last_id_db)
        datadf = get_data(last_id_db, limit=1000)
        if len(datadf) == 0:
            print('no more data')
            break

        last_id_db = datadf['id'].tolist()[-1]

        data = []
        for indx, row in datadf.iterrows():
            curdata = {'filename': row['name'],
                       'username': row['truename'],
                       'sizeByte': row['filesize'],
                       'sizeMb': row['filesize'] / (1024 * 1024),
                       'timestamp': int(row['createtime'].timestamp()),
                       'filetype': os.path.splitext(row['name'])[-1],
                       'type': '',
                       'haslabel': 0}

            for lb in labels:
                if lb in row['name']:
                    curdata['type'] = lb
                    curdata['haslabel'] = 1
                    break

            # pics
            if not curdata['type']:
                if 'image' in row['filetype']:  # or 'jpeg' in row['filetype']
                    curdata['type'] = '图片'
                else:
                    curdata['type'] = 'NoType'

            data.append(curdata)

        # print(data)
        send_data(data)
        print('send', len(data), 'to', last_id_db)

    print('end')


def send_data(value):
    producer = KafkaProducer(bootstrap_servers=['testdb.ibuildingsh.com:9092'])

    data = {'source_id': '6012283db2296c000167711d',
            'key': 'document-data',
            'value': value}

    future = producer.send(
        topic='t-document-data',
        key='document-data'.encode('utf-8'),
        # key=str(datetime.now()).encode('utf-8'),
        value=json.dumps(data).encode('utf-8'),
        partition=0)

    producer.close()


def test_data():
    producer = KafkaProducer(bootstrap_servers=['testdb.ibuildingsh.com:9092'])
    # , security_protocol="SSL"

    types = ['doc', 'pdf', 'ppt']
    filetypes = ['施工', '运维', '进度', '方案']
    usernames = ['我', '你', '你', '他']

    data = {'source_id': '6010c605186e4e0001e27ab1',
            'key': 'test-file',
            'value': []}

    for i in range(10):
        cursize = np.random.rand() * 100
        value = {'filetype': np.random.choice(filetypes),
                 'filename': str(i + 300000),
                 'type': np.random.choice(types),
                 'sizeMb': int(cursize),
                 'sizeByte': int(cursize * 1024 * 1024),
                 'username': np.random.choice(usernames),
                 'timestamp': int(datetime(year=2021, month=1, day=np.random.randint(1, 19)).timestamp())}
        data['value'].append(value)

    future = producer.send(
        topic='t-file-data-multi',
        key='file-test-multi'.encode('utf-8'),
        # key=str(datetime.now()).encode('utf-8'),
        value=json.dumps(data).encode('utf-8'),
        partition=0)

    # result = future.get(timeout=10)
    # print(data)
    producer.close()


if __name__ == '__main__':
    recalculate()
    # test_data()
    # save_names()
    # calculate_labels()
