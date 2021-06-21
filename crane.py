import re, os
from collections import Counter
from kafka import KafkaProducer
import time, json
from datetime import datetime
import numpy as np
import pandas as pd
from sqlalchemy import create_engine


def get_data(lastid=-1, limit=100):
    constr = "mysql+pymysql://yufq007:shsijian007@rdsira6v2ira6v2public.mysql.rds.aliyuncs.com:3307/swcs1"
    conn = create_engine(constr).connect()
    query = '''SELECT id,towercrane_id,Angle,Radius,Height,`Load`,
                MomentPer,WindSpeed,PreAlarm,Alarm,CollectionTime AS time
                FROM `monitor_towercranelive`
                WHERE str_to_date(CollectionTime,'%%Y-%%m-%%d %%H:%%i:%%s')>'2020-1-1'
                AND towercrane_id=53 AND id>{} LIMIT {}
            '''.format(lastid, limit)
    return pd.read_sql_query(query, conn)


# 从头计算写入
def recalculate():
    # last_id_db = -1
    last_id_db = 547023
    tol = 3
    while True:
        print('last ', last_id_db)
        datadf = get_data(last_id_db, limit=10000)
        if len(datadf) == 0:
            print('no more data')
            break

        last_id_db = datadf['id'].tolist()[-1]

        datadf = datadf.drop_duplicates(subset=['time'])
        datadf['timestamp'] = datadf['time'].astype('datetime64')
        del datadf['time']

        # u_angle, d_angle = np.percentile(datadf['Angle'], 100 - tol), np.percentile(datadf['Angle'], tol)
        # u_radius, d_radius = np.percentile(datadf['Radius'], 100 - tol), np.percentile(datadf['Radius'], tol)
        # u_height, d_height = np.percentile(datadf['Height'], 100 - tol), np.percentile(datadf['Height'], tol)
        # u_load, d_load = np.percentile(datadf['Load'], 100 - tol), np.percentile(datadf['Load'], tol)
        # u_moment, d_moment = np.percentile(datadf['MomentPer'], 100 - tol), np.percentile(datadf['MomentPer'], tol)
        # u_wind, d_wind = np.percentile(datadf['WindSpeed'], 100 - tol), np.percentile(datadf['WindSpeed'], tol)

        u_angle, d_angle = np.percentile(datadf['Angle'], 100 - tol), np.percentile(datadf['Angle'], tol)
        u_radius, d_radius = np.percentile(datadf['Radius'], 100 - tol * 2), np.percentile(datadf['Radius'], 0)
        u_height, d_height = np.percentile(datadf['Height'], 100 - tol * 2), np.percentile(datadf['Height'], 0)
        u_load, d_load = np.percentile(datadf['Load'], 100 - tol * 2), np.percentile(datadf['Load'], 0)
        u_moment, d_moment = np.percentile(datadf['MomentPer'], 100 - tol * 2), np.percentile(datadf['MomentPer'], 0)
        u_wind, d_wind = np.percentile(datadf['WindSpeed'], 100 - tol * 2), np.percentile(datadf['WindSpeed'], 0)

        def process_row(y):
            y['AngleDiff'] = abs(180 - y['Angle'])
            y['timestamp'] = int(y['timestamp'].timestamp())

            if y['Alarm'] > 0 or y['PreAlarm'] > 0:
                y['abnormal'] = 2
                return y

            count = 0
            if y['Angle'] > u_angle or y['Angle'] < d_angle:
                count += 1
            if y['Radius'] > u_radius or y['Radius'] < d_radius:
                count += 1
            if y['Height'] > u_height or y['Height'] < d_height:
                count += 2
            if y['Load'] > u_load or y['Load'] < d_load:
                count += 0.1
            if y['MomentPer'] > u_moment or y['MomentPer'] < d_moment:
                count += 2
            if y['WindSpeed'] > u_wind or y['WindSpeed'] < d_wind:
                count += 1

            if count > 3:
                y['abnormal'] = 1
            else:
                y['abnormal'] = 0

            return y

        datadf = datadf.apply(process_row, axis=1)

        watch = datadf[datadf['abnormal'] > 0]
        print('abnormal rate {}'.format(len(watch) / len(datadf)))

        data = datadf.to_dict('records')
        batch = 500
        data_split = np.split(np.array(data), np.array(range(1, int(len(data) / batch) + 1)) * batch)
        for b in data_split:
            send_data(list(b))
            print('batch send to {}'.format(b[-1]['id']))

        # pos = -1
        # sending = []
        # while True:
        #     pos += 1
        #     if pos > len(data):
        #         break
        #     if len(sending) < 100 and len(data) - pos >= 100:
        #         sending.append(data[pos])
        #     else:
        #         if sending:
        #             send_data(sending)
        #         sending = []

        print('send {} to {}'.format(len(datadf), last_id_db))
        print()

    print('end')


def send_data(value):
    producer = KafkaProducer(bootstrap_servers=['testdb.ibuildingsh.com:9092'])

    data = {
        'source_id': '604a131b71dddd0001c1dab5',
        # 'source_id': '60471bc04d94d2000129f61f',
        'key': 'towercrane-analysis',
        'value': value,
    }

    future = producer.send(
        topic='t-towercrane-analysis',
        key='towercrane-analysis'.encode('utf-8'),
        # key=str(datetime.now()).encode('utf-8'),
        value=json.dumps(data).encode('utf-8'),
        partition=0)

    producer.close()


if __name__ == '__main__':
    recalculate()
    # test_data()
    # save_names()
    # calculate_labels()
