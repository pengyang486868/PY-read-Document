import pdfplumber


# import pandas as pd
def readtext(full_path):
    result = []
    with pdfplumber.open(full_path) as pdf:
        for p in pdf.pages:
            text = p.extract_text()
            textarr = text.split('\n')
            # 还需猜测文档一般行字数 合并句尾分段
            result.append(textarr)
        # table = page.extract_tables()
        # for t in table:
        #     df = pd.DataFrame(t[1:], columns=t[0])

    return result
