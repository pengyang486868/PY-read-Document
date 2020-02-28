import pdfplumber


# import pandas as pd
def readtext(full_path):
    result = []
    with pdfplumber.open(full_path) as pdf:
        for p in pdf.pages:
            text = p.extract_text()
            # table = page.extract_tables()
            textarr = text.split('\n')
            # 还需猜测文档一般行字数 合并句尾分段

            result.append(textarr)

    return result
