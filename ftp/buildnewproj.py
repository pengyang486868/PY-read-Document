from cloudservice import add_proj_simple
import pandas as pd


def testadd():
    pname = '施工项目1'
    pnumber = '404'
    pstage = '施工'
    parea = 10000
    add_proj_simple(pname, pnumber, pstage, parea)


def do_add_ftp_projs():
    data = pd.read_csv(r'.\ftpnewproj.csv')
    data['writename'] = data['name'].apply(lambda x: x.split(' ')[1].split('-')[0])
    for indx, row in data.iterrows():
        pname = row['writename']
        pnumber = row['name'] + '/' + str(row['sub'])
        pstage = '施工'
        parea = 23100
        add_proj_simple(pname, pnumber, pstage, parea)
        print(pnumber)


if __name__ == '__main__':
    # testadd()
    do_add_ftp_projs()
