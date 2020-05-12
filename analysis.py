import pandas as pd
from cloudservice import get_documenttask, download_doc
from cloudservice import get_doctag, create_doctag, delete_doctag
from cloudservice import create_doctagrel


def test():
    docresponse = get_documenttask()
    docdata = pd.DataFrame(docresponse)

    # only proj4
    docdata = docdata[docdata['projectId'] == 4]

    docdata = (docdata.sort_values('name')
               .dropna(subset=['fileUrl', 'step'])
               .reset_index()
               )

    utest = docdata['fileUrl'].tolist()[0]
    dname = docdata['name'].tolist()[0]
    # download_doc(utest, 'D:\\' + dname)

    r1 = create_doctag('关联r1')
    r2 = create_doctag('关联r2')
    # r = delete_doctag(1)
    allt = get_doctag()
    create_doctagrel([(10, r1), (15, r2)])
    print()


if __name__ == '__main__':
    test()
