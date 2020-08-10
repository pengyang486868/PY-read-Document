from pathlib import Path
import numpy as np
import pandas as pd
from cloudservice import get_file_projs, get_all_projs


def test():
    dpath = Path(r'\\192.168.11.70\工程资料 01\01 工程资料')
    result = []
    for thing in dpath.iterdir():
        if thing.is_dir():
            for dthing in thing.iterdir():
                if dthing.is_dir():
                    dname = str(dthing)
                    splt = dname.split('\\')
                    result.append([splt[-2], splt[-1]])
    print(result)
    np.savetxt('projs1.csv', result, delimiter=',', fmt='%s')


def now_have_file_projs():
    ps = get_file_projs(onlyid=True)
    ps = pd.DataFrame(ps, columns=['havef'])
    allp = get_all_projs()
    allp = pd.DataFrame(allp)

    allp = pd.merge(allp, ps, how='inner', left_on='id', right_on='havef')

    return allp[['id', 'name']]


if __name__ == "__main__":
    # \\192.168.11.70\工程资料 01\01 工程资料\402\040 中信泰富-杜晓晖
    # ftp = ftpconnect("192.168.11.70", str("余芳强".encode('utf-8')), "16728227")
    # downloadfile(ftp, "Faint.mp4", "C:/Users/Administrator/Desktop/test.mp4")
    # uploadfile(ftp, "C:/Users/Administrator/Desktop/test.mp4", "test.mp4")
    # ftp.quit()
    print(now_have_file_projs())
