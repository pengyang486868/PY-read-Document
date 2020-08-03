import utils
import numpy as np
import re


def test1():
    print(ord('z'))
    print(ord('2'))
    print(utils.is_pure_abc('jgjw12'))
    print(utils.is_pure_abc('jgjw我12'))
    x = [None]
    a = [1, 2, 3]
    a += x
    print(a)


def test_pytorch():
    import torch
    from torch.autograd import Variable
    from torch import nn

    net_out = Variable(torch.Tensor([[7.9990e-04, 2.1942e-04, 9.9931e-01, 6.3310e-04, 1.1731e-04]]))
    target = Variable(torch.LongTensor([2]))

    criterion = nn.CrossEntropyLoss()
    ret = criterion(net_out, target)
    print(ret)


def test2():
    from ocrapi import baidu as ocr
    s = ocr.img_to_str(r'D:\filedata/ocrtest.jpg')
    print(s)


def test3():
    import utils
    s = utils.get_namedwords(['案例介绍：      某厂施工中的文化活动站的观众厅，于某年4月14日下午因墙体失稳，拱形钢筋混凝土屋盖塌落，造成了重大事故。'])
    print(s)


def test4():
    a = np.linalg.norm(np.array([1, 2, 3]) - np.array([2, 3, 5]))
    print(a)


def test5():
    s = r'{\H1.3333x;\P一、设计依据\P}    1.工程概况  \P    本工程为{\C3;甲类}民防工程，位于地下{\C3;二、三}层，' \
        '平时为地下汽车库和医院配套用房；临战%%转换为{\C3;3}个甲类常6级核6级二等人员掩蔽部（防化级别为丙级）、' \
        '{\C3;1}个甲类核5级常5级急救医院（防化级别%%为乙级）和{\C3;1}座固定柴油电站，共设{\C3;4}个防护单元。      \P    ' \
        '本工程耐火等级为一级，防化级别为乙级和丙级，本设计为仅战时功能设计。\P    2.建筑和有关专业提供的作业图和有关资料' \
        '；\P    3.政府主管部门初步设计的审批意见{\C3; };\P    4.建设单位提供的本工程有关资料和设计任务委托书；  \P    5.与' \
        '合作单位的设计任务分工表；\P    6.现行的国家和地方有关规范、规程、标准：\P    《低压配'

    r = utils.remove_cadliteral(s)
    print(r)


def test6():
    import torch
    print(torch.nn.MSELoss)


def test7():
    import os
    decide = os.path.isfile(r'D:\filedata\new.txt')
    print(decide)


def test8():
    import pandas as pd
    from datetime import datetime
    data = pd.DataFrame([['2017-01-03 09:01:00 2017-01-03', 2888], ['2017-01-03 09:02:00 2017-01-03', 2999]],
                        columns=['date', 'whatever'])
    data['time'] = data['date'].apply(lambda x: datetime.strptime(x.split()[1], '%H:%M:%S'))
    data['hour'] = data['time'].apply(lambda x: x.hour)
    data['minute'] = data['time'].apply(lambda x: x.minute)

    print(data)


class 牛人:
    def __init__(self, 输入的名字):
        self.名字 = 输入的名字

    def 嚎(self):
        print('我是牛人 ' + self.名字)


if __name__ == '__main__':
    林松 = 牛人('林松啊')
    林松.嚎()
