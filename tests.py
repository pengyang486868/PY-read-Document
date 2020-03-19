import utils
import numpy as np


def test1():
    print(ord('z'))
    print(ord('2'))
    print(utils.is_pure_abc('jgjw12'))
    print(utils.is_pure_abc('jgjw我12'))


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


def test4():
    a = np.linalg.norm(np.array([1, 2, 3]) - np.array([2, 3, 5]))
    print(a)


if __name__ == '__main__':
    test4()
