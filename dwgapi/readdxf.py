import dxfgrabber
import utils


def read(full_path):
    dxf = dxfgrabber.readfile(full_path)
    for layer in dxf.layers:
        print(layer.name, layer.color, layer.linetype)

    for l in dxf.entities:
        curstr = ''
        if l.dxftype == 'MTEXT':
            # print(l.insert)
            curstr = l.raw_text
        if l.dxftype == "TEXT":
            # print(round(l.insert[0], 2))
            curstr = l.text
        if curstr and (not utils.is_pure_abc(curstr)):
            print(curstr)
