from win32com import client
import os


def ppt2pptx(path: str, newdir: str, remove=False):
    if not path.endswith('.ppt'):
        return False, None
    w = client.Dispatch('PowerPoint.Application')
    w.Visible = 1
    w.DisplayAlerts = 0

    doc = w.Presentations.Open(path)
    # newpath = path + 'x'
    newpath = os.path.join(newdir, os.path.split(path)[1] + 'x')
    doc.SaveAs(newpath)
    doc.Close()
    w.Quit()

    if remove:
        os.remove(path)
    return True, newpath
