from aip import AipOcr

config = {
    'appId': '16804814',
    'apiKey': 'mVCRu8AmAcTdFSGaDtoRki53',
    'secretKey': '48BFM2ZXRf8yF7cFIP5nXLNwQKYoiOHz'
}

client = AipOcr(**config)


def get_file_content(file):
    with open(file, 'rb') as fp:
        return fp.read()
