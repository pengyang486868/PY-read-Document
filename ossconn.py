import oss2
from urllib import request
import json, os
from config import backendserver
import uuid


def get_oss_info():
    url = backendserver + '/api/osstoken'
    req = request.Request(url, headers={})
    f = request.urlopen(req)
    cdata = str(f.read().decode())
    return json.loads(cdata)


def upload_to_oss(fpath, prefix='ATTA_', fobjname=None):
    if not fobjname:
        # fobjname = os.path.split(fpath)[1]
        extname = os.path.splitext(fpath)[-1]
        fobjname = prefix + str(uuid.uuid4()) + extname
    oss_info = get_oss_info()

    # 'http://oss-cn-hangzhou.aliyuncs.com'
    oss_region_url = 'http://' + oss_info['region'] + '.aliyuncs.com'
    # auth = oss2.Auth(oss_info['accessKeyId'], oss_info['accessKeySecret'])
    auth = oss2.StsAuth(oss_info['accessKeyId'], oss_info['accessKeySecret'], oss_info['stsToken'])
    bucket = oss2.Bucket(auth, oss_region_url, oss_info['bucket'])

    # # 必须以二进制的方式打开文件，因为需要知道文件包含的字节数。
    # with open('<yourLocalFile>', 'rb') as fileobj:
    #     # Seek方法用于指定从第1000个字节位置开始读写。上传时会从您指定的第1000个字节位置开始上传，直到文件结束。
    #     fileobj.seek(1000, os.SEEK_SET)
    #     # Tell方法用于返回当前位置。
    #     current = fileobj.tell()
    #     bucket.put_object('<yourObjectName>', fileobj)

    response_obj = bucket.put_object_from_file(fobjname, fpath)
    expire = 60 * 60 * 24 * 365 * 100  # 100 year
    signed = bucket.sign_url('GET', fobjname, expire, slash_safe=True)
    return signed.split('?')[0]

