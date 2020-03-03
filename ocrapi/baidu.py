import numpy as np
import os
from .common import client
from .common import get_file_content


def img_to_str(image_path):
    image = get_file_content(image_path)
    res = client.basicAccurate(image)
    if 'words_result' in res:
        # return '\n'.join([w['words'] for w in res['words_result']])
        return [w['words'] for w in res['words_result']]
    return ''


# path = r'D:\ocrs'
# name = 'gy3.jpg'
# result = img_to_str(os.path.join(path, name))
# np.savetxt(os.path.join(path, name + '-result.txt'), np.array([result]), delimiter='', fmt='%s')
# print(result)
