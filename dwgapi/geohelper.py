from typing import Tuple
import math
from fileenum import DxfType


# national standard length
def is_standard_frame_len(length, rng=10000) -> bool:
    nrange = 30
    if length < rng / nrange:
        return False

    gbstandard = [210, 297, 420, 594, 841, 1189]  # GB standard
    scale = [1, 2, 5, 10, 20, 50] + [100 * x for x in range(1, 20)]
    compare = [length / x for x in scale]
    tol = 0.1
    for s in gbstandard:
        for c in compare:
            if abs(s - c) < tol:
                return True
    return False


# whether \sqrt(2)
def is_standard_frame(hlinelen, vlinelen) -> Tuple[bool, str]:
    kind = 'h'  # default: horizontal frame
    if hlinelen < vlinelen:  # possibly verticle frame
        kind = 'v'
        vlinelen, hlinelen = hlinelen, vlinelen
    tol = 0.01 * vlinelen
    if abs(vlinelen * math.sqrt(2) - hlinelen) < tol:
        return True, kind
    return False, kind


def ishorizontal(start, end) -> bool:
    tol = 1
    if abs(start[1] - end[1]) < tol:
        return True
    return False


def isverticle(start, end) -> bool:
    tol = 1
    if abs(start[0] - end[0]) < tol:
        return True
    return False


# bounding box for lines
def bboxfor(e, dxftype=DxfType.LINE):
    xmin = float('inf')
    xmax = float('-inf')
    ymin = float('inf')
    ymax = float('-inf')
    if dxftype == DxfType.LINE:
        xmax = max(e.start[0], e.end[0], xmax)
        xmin = min(e.start[0], e.end[0], xmin)
        ymax = max(e.start[1], e.end[1], ymax)
        ymin = max(e.start[1], e.end[1], ymin)
    if dxftype == DxfType.LWPOLYLINE:
        for p in e.points:
            xmax = max(p[0], xmax)
            xmin = min(p[0], xmin)
            ymax = max(p[1], ymax)
            ymin = min(p[1], ymin)
    return xmin, xmax, ymin, ymax


# block overall range
def bbox_block(b):
    range_xmin = float('inf')
    range_xmax = float('-inf')
    range_ymin = float('inf')
    range_ymax = float('-inf')
    for e in b:
        cur_xmin, cur_xmax, cur_ymin, cur_ymax = bboxfor(e, e.dxftype)
        range_xmin = min(cur_xmin, range_xmin)
        range_xmax = max(cur_xmax, range_xmax)
        range_ymin = min(cur_ymin, range_ymin)
        range_ymax = max(cur_ymax, range_ymax)
    return range_xmin, range_xmax, range_ymin, range_ymax
