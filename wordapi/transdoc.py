from win32com import client
import os


def doc2docx(path: str, remove=False):
    if not path.endswith('.doc'):
        return False, None
    w = client.Dispatch('Word.Application')
    w.Visible = 0
    w.DisplayAlerts = 0

    doc = w.Documents.Open(path)
    newpath = path + 'x'
    doc.SaveAs(newpath, 16, False, "", True, "", False, False, False, False)
    doc.Close()
    w.Quit()

    if remove:
        os.remove(path)
    return True, newpath
