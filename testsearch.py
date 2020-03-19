from docDAL import mysql as conn
import core

searchq = True
if searchq:
    fobjs = conn.get_file_info(returnobj=True)
    # bs1, time1 = core.search_basic('安全 施工 人员 熊猫环岛', fobjs, givetime=True)
    # bs2, time2 = core.search_basic('BIM 管理 模块 消防', fobjs)
    rs1 = core.recommand(fobjs[2], fobjs, rnum=20)
    rs2 = core.recommand(fobjs[18], fobjs, rnum=20)

    # imgobjs = conn.get_img_info(returnobj=True)
    # is1, time3 = core.search_img('安全 工程 熊猫环岛', imgobjs)
    # is2, time4 = core.search_img('BIM 管理', imgobjs)

    # ns1, time3 = core.search_natural('管理和运维', fobjs)
    # ns2, time4 = core.search_natural('安全生产文明施工的文档', fobjs)
    print()
