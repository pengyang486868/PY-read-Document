from docDAL import mysql as conn
import core

simple_search_q = True
recommand_q=False
img_search_q=False
nlp_search_q=False

fobjs = conn.get_file_info(returnobj=True)

if simple_search_q:
    bs1, time1 = core.search_basic('进度 质量 控制', fobjs, givetime=True)
    # bs2, time2 = core.search_basic('应当 设备', fobjs)

if recommand_q:
    rs1 = core.recommand(fobjs[2], fobjs, rnum=20)
    rs2 = core.recommand(fobjs[18], fobjs, rnum=20)

if img_search_q:
    imgobjs = conn.get_img_info(returnobj=True)
    is1, time3 = core.search_img('安全 工程 熊猫环岛', imgobjs)
    is2, time4 = core.search_img('BIM 管理', imgobjs)

if nlp_search_q:
    ns1, time3 = core.search_natural('管理和运维', fobjs)
    ns2, time4 = core.search_natural('安全生产文明施工的文档', fobjs)

print()
