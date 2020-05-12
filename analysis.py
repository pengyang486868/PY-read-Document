import pandas as pd
from cloudservice import get_documenttask, download_doc
from cloudservice import get_doctag, create_doctag, delete_doctag
from cloudservice import create_doctagrel, delete_doctagrel
import time


def test():
    docresponse = get_documenttask(projid=4)
    docdata = pd.DataFrame(docresponse)

    docdata = (docdata.sort_values('name')
               .dropna(subset=['fileUrl', 'step'])
               .reset_index()
               )

    utest = docdata['fileUrl'].tolist()[0]
    dname = docdata['name'].tolist()[0]
    # download_doc(utest, 'D:\\' + dname)

    r1 = create_doctag('混凝土', projid=4)
    r2 = create_doctag('施工', projid=4)
    # r = delete_doctag(1)
    # allt = get_doctag()
    create_doctagrel([(155, r1), (155, r2)], projid=4)
    print()


def on_loop(project_id):
    # docresponse = get_documenttask(projid=project_id)
    # docdata = pd.DataFrame(docresponse)
    # docdata = docdata[docdata['step'] == 1]
    #
    # docdata = (docdata.sort_values('name')
    #            .dropna(subset=['fileUrl', 'step'])
    #            .reset_index()
    #            )
    #
    # # download_doc(utest, 'D:\\' + dname)
    #
    # r = create_doctag('混凝土', projid=project_id)
    # # allt = get_doctag()
    # create_doctagrel([(155, r), (155, r)], projid=project_id)

    delete_doctagrel(13, projid=project_id)


if __name__ == '__main__':
    for _ in range(1):
        on_loop(project_id=4)
        time.sleep(5)
