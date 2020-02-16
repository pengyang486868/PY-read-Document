import dxfgrabber


def read(full_path):
    dxf = dxfgrabber.readfile(full_path)
    for layer in dxf.layers:
        print(layer.name, layer.color, layer.linetype)

    for l in dxf.entities:
        if l.dxftype == 'MTEXT':
            print(l.raw_text)
            # print(l.insert)
        if l.dxftype == "TEXT":
            print(l.text)
            # print(round(l.insert[0], 2))
