import re, os
from collections import Counter
from kafka import KafkaProducer
import time, json
from datetime import datetime
import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def get_data():
    pth = r'E:\work\课题\工业互联网执行阶段\指标完成\motor.csv'
    d = pd.read_csv(pth)
    d = d.melt(id_vars='time', var_name='name', value_name='work_hour').dropna(subset=['work_hour'])

    def process(row):
        row['load'] = np.random.rand() * 13
        row['abnormal'] = 1 if np.random.random() > 0.9 else 0
        row['rate'] = 100 if np.random.random() > 0.1 else 0
        return row

    d = d.apply(process, axis=1)

    save = r'E:\work\课题\工业互联网执行阶段\指标完成\motor_info.csv'
    d.to_csv(save, encoding='utf-8')

    return d


# 从头计算写入
def recalculate():
    pth = r'E:\work\课题\工业互联网执行阶段\指标完成\motor_info.csv'
    datadf = pd.read_csv(pth)
    datadf['timestamp'] = datadf['time'].astype('datetime64')

    def transtime(y):
        y['timestamp'] = int(y['timestamp'].timestamp())
        return y

    datadf = datadf.apply(transtime, axis=1)

    data = datadf.to_dict('records')
    send_data(data)

    print('end')


def send_data(value):
    producer = KafkaProducer(bootstrap_servers=['testdb.ibuildingsh.com:9092'])

    data = {
        'source_id': '6052c230c8dc420001ef5ffc',
        # 'source_id': '60471bc04d94d2000129f61f',
        'key': 'truck-crane',
        'value': value,
    }

    future = producer.send(
        topic='t-truck-crane',
        key='truck-crane'.encode('utf-8'),
        # key=str(datetime.now()).encode('utf-8'),
        value=json.dumps(data).encode('utf-8'),
        partition=0)

    producer.close()


if __name__ == '__main__':
    # get_data()
    recalculate()
