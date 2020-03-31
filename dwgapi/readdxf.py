import dxfgrabber
from .geohelper import *
import fileenum


def read_example(full_path):
    dxf = dxfgrabber.readfile(full_path)
    # for layer in dxf.layers:
    #     print(layer.name, layer.color, layer.linetype)

    hlens = []
    vlens = []
    for e in dxf.entities:
        if e.dxftype == 'INSERT':
            if e.name.startswith('A$'):
                print(e.name)
        # curstr = ''
        # if l.dxftype == 'MTEXT':  # print(l.insert)
        #     curstr = l.raw_text
        # if l.dxftype == "TEXT":  # print(round(l.insert[0], 2))
        #     curstr = l.text
        # if curstr and (not utils.is_pure_abc(curstr)):
        #     print(curstr)
        if e.dxftype == 'LINE':
            if ishorizontal(e.start, e.end):
                linelen = abs(e.start[0] - e.end[0])
                hlens.append(linelen)
            if isverticle(e.start, e.end):
                linelen = abs(e.start[1] - e.end[1])
                vlens.append(linelen)

    for b in dxf.blocks:
        for e in b:
            if e.dxftype == 'LINE':
                if ishorizontal(e.start, e.end):
                    linelen = abs(e.start[0] - e.end[0])
                    hlens.append(linelen)
                if isverticle(e.start, e.end):
                    linelen = abs(e.start[1] - e.end[1])
                    vlens.append(linelen)
            if e.dxftype == 'LWPOLYLINE':
                for indx, p in enumerate(e.points):
                    if not e.is_closed:
                        if indx == len(e) - 1:
                            break
                    nextp = e.points[int((indx + 1) % len(e))]
                    if ishorizontal(p, nextp):
                        linelen = abs(p[0] - nextp[0])
                        hlens.append(linelen)
                    if isverticle(p, nextp):
                        linelen = abs(p[1] - nextp[1])
                        vlens.append(linelen)

    hlens.sort(reverse=True)
    vlens.sort(reverse=True)
    print()


# all in dxf.modelspace()
def split_drawing(full_path):
    dxf = dxfgrabber.readfile(full_path)

    # guess overall range
    range_xmin = float('inf')
    range_xmax = float('-inf')
    range_ymin = float('inf')
    range_ymax = float('-inf')
    for e in dxf.modelspace():
        if e.dxftype == 'LINE':
            if e.start[0] > range_xmax:
                range_xmax = e.start[0]
            if e.start[0] < range_xmin:
                range_xmin = e.start[0]
            if e.start[1] > range_ymax:
                range_ymax = e.start[1]
            if e.start[1] < range_ymin:
                range_ymin = e.start[1]

    range_drawing = (range_xmax - range_xmin + range_ymax - range_ymin) / 2

    hlens = []
    vlens = []
    for e in dxf.modelspace():
        # if e.dxftype == 'INSERT':
        #     if e.name.startswith('A$'):
        #         print(e.name)
        if e.dxftype == 'LINE':
            if ishorizontal(e.start, e.end):
                linelen = abs(e.start[0] - e.end[0])
                hlens.append(linelen)
            if isverticle(e.start, e.end):
                linelen = abs(e.start[1] - e.end[1])
                vlens.append(linelen)

    for b in dxf.blocks:
        for e in b:
            if e.dxftype == 'LINE':
                if ishorizontal(e.start, e.end):
                    linelen = abs(e.start[0] - e.end[0])
                    hlens.append(linelen)
                if isverticle(e.start, e.end):
                    linelen = abs(e.start[1] - e.end[1])
                    vlens.append(linelen)
            if e.dxftype == 'LWPOLYLINE':
                for indx, p in enumerate(e.points):
                    if not e.is_closed:
                        if indx == len(e) - 1:
                            break
                    nextp = e.points[int((indx + 1) % len(e))]
                    if ishorizontal(p, nextp):
                        linelen = abs(p[0] - nextp[0])
                        hlens.append(linelen)
                    if isverticle(p, nextp):
                        linelen = abs(p[1] - nextp[1])
                        vlens.append(linelen)

    hlens.sort(reverse=True)
    vlens.sort(reverse=True)

    hlen_standard = []
    vlen_standard = []
    for hl in hlens:
        if is_standard_frame_len(hl, range_drawing):
            hlen_standard.append(hl)
    for vl in vlens:
        if is_standard_frame_len(vl, range_drawing):
            vlen_standard.append(vl)

    vlen_standard = list(set([int(x) for x in vlen_standard]))
    hlen_standard = list(set([int(x) for x in hlen_standard]))

    for vlen in vlen_standard:
        for hlen in hlen_standard:
            is_standard, standard_kind = is_standard_frame(hlinelen=hlen, vlinelen=vlen)
            if is_standard:
                print(vlen, hlen, standard_kind)

    print()


def readtxt(full_path):
    return ['']


# Splitting drawing if frame is 'BLOCK'
def split_drawing_byblock(full_path):
    dxf = dxfgrabber.readfile(full_path)

    sbcoords = []  # standard block coordinates: left right bottom top
    sblock_names = []  # standard block names
    for b in dxf.blocks:
        range_xmin, range_xmax, range_ymin, range_ymax = bbox_block(b)
        brange_x = range_xmax - range_xmin
        brange_y = range_ymax - range_ymin

        # length should be standard & w/h should be \sqrt(2)
        if not is_standard_frame_len(brange_x):
            continue
        is_standard, standard_kind = is_standard_frame(hlinelen=brange_x, vlinelen=brange_y)

        # add to result
        if is_standard:
            print('检测到的标准图框的块', brange_x, brange_y, b.name, standard_kind)
            sblock_names.append(b.name)
            # left right bottom top
            sbcoords.append([range_xmin, range_xmax, range_ymin, range_ymax])

    terminal_blocks = []  # final block of standard blocks, maybe itself
    for sbname in sblock_names:
        deltax = 0
        deltay = 0
        while True:
            found = False
            for b in dxf.blocks:
                for ins in filter(lambda x: x.dxftype == DxfType.INSERT, b):
                    if ins.name == sbname:
                        # coor history record
                        deltax += ins.insert[0]
                        deltay += ins.insert[1]
                        found = True
                        sbname = b.name
            if found is not True:
                terminal_blocks.append([sbname, deltax, deltay])
                break

    print('最初图块在最终图块的累积偏移', terminal_blocks)

    split_result = []
    for tb, sbc in zip(terminal_blocks, sbcoords):
        for e in filter(lambda x: x.dxftype == DxfType.INSERT, dxf.entities):
            if e.name == tb[0]:
                # left right bottom top
                offset = 2
                split_result.append({'left': int(sbc[0] + tb[1] + e.insert[0] - offset),
                                     'right': int(sbc[1] + tb[1] + e.insert[0] + offset),
                                     'bottom': int(sbc[2] + tb[2] + e.insert[1] - offset),
                                     'top': int(sbc[3] + tb[2] + e.insert[1] + offset)})

    print('最初图块的左右下上', sbcoords)
    print('最终坐标系的左右下上', split_result)
    return split_result
