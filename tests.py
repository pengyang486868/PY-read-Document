import utils

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


from ocrapi import baidu as ocr

s = ocr.img_to_str(r'D:\filedata/ocrtest.jpg')
print(s)
