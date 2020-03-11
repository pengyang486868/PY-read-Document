from win32com import client
import os
import shutil

def doc2docx(path: str, newdir: str, remove=False):
    if not path.endswith('.doc'):
        return False, None
    w = client.Dispatch('Word.Application')
    w.Visible = 0
    w.DisplayAlerts = 0

    doc = w.Documents.Open(path)
    # newpath = path + 'x'
    # newpath = os.path.join(newdir, os.path.split(path)[1] + 'x')
    noext = os.path.join(newdir, os.path.splitext(os.path.split(path)[1])[0])
    newpath = noext + '.htm'
    doc.SaveAs2(newpath, 8)  # , False, "", True, "", False, False, False, False
    # doc.SaveAs2(newpath, 16, False, '', True, '', False, True, True, True, True, None, False, False, 4, True, 15)
    doc.Close()

    dochtml = w.Documents.Open(newpath)
    dochtml.SaveAs2(noext + '.docx', 16)

    w.Quit()

    # remove html middle files
    os.remove(newpath)
    shutil.rmtree(noext + '.files')

    # remove raw file or not
    if remove:
        os.remove(path)
    return True, newpath
