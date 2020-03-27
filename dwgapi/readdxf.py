import dxfgrabber
import utils
from typing import Tuple
import math


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


# frame block split
def split_drawing_byblock(full_path):
    dxf = dxfgrabber.readfile(full_path)

    branges = []

    for b in dxf.blocks:
        # block overall range
        range_xmin = float('inf')
        range_xmax = float('-inf')
        range_ymin = float('inf')
        range_ymax = float('-inf')
        for e in b:
            if e.dxftype == 'LINE':
                if e.start[0] > range_xmax:
                    range_xmax = e.start[0]
                if e.start[0] < range_xmin:
                    range_xmin = e.start[0]
                if e.start[1] > range_ymax:
                    range_ymax = e.start[1]
                if e.start[1] < range_ymin:
                    range_ymin = e.start[1]
            if e.dxftype == 'LWPOLYLINE':
                for p in e.points:
                    if p[0] > range_xmax:
                        range_xmax = p[0]
                    if p[0] < range_xmin:
                        range_xmin = p[0]
                    if p[1] > range_ymax:
                        range_ymax = p[1]
                    if p[1] < range_ymin:
                        range_ymin = p[1]
        branges.append((range_xmax - range_xmin, range_ymax - range_ymin, b.name))

    sblock_names = []
    for rng in branges:
        if not is_standard_frame_len(rng[0]):
            continue
        is_standard, standard_kind = is_standard_frame(hlinelen=rng[0], vlinelen=rng[1])
        if is_standard:
            print(rng, standard_kind)
            sblock_names.append(rng[2])

    terminal_blocks = []
    for sbname in sblock_names:
        while True:
            found = False
            for b in dxf.blocks:
                for insert in filter(lambda x: x.dxftype == 'INSERT', b):
                    if insert.name == sbname:
                        found = True
                        sbname = b.name
            if found is not True:
                terminal_blocks.append(sbname)
                break

    print(terminal_blocks)

    # zuobiao bianhuan record
    drawing_inserts = []
    for tb in terminal_blocks:
        for e in filter(lambda x: x.dxftype == 'INSERT', dxf.entities):
            if e.name == tb:
                drawing_inserts.append(e)

    print(drawing_inserts)


def is_standard_frame_len(length, rng=10000):
    nrange = 10
    if length < rng / nrange:
        return False

    gbstandard = [210, 297, 420, 594, 841, 1189]
    scale = [1, 2, 5, 10, 20, 50] + [100 * x for x in range(1, 20)]
    compare = [length / x for x in scale]
    tol = 0.1
    for s in gbstandard:
        for c in compare:
            if abs(s - c) < tol:
                return True
    return False


def is_standard_frame(hlinelen, vlinelen) -> Tuple[bool, str]:
    kind = 'h'  # default: horizontal frame
    if hlinelen < vlinelen:  # possibly verticle frame
        kind = 'v'
        vlinelen, hlinelen = hlinelen, vlinelen
    tol = 0.01 * vlinelen
    if abs(vlinelen * math.sqrt(2) - hlinelen) < tol:
        return True, kind
    return False, kind


def ishorizontal(start, end):
    tol = 1
    if abs(start[1] - end[1]) < tol:
        return True
    return False


def isverticle(start, end):
    tol = 1
    if abs(start[0] - end[0]) < tol:
        return True
    return False
