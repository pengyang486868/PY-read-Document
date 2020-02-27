def read(full_path):
    with open(full_path, encoding='utf-8') as f:
        s = f.read()
        s = s.split('\n')

    # 去掉空的段落
    content = []
    for e in s:
        if e:
            content.append(e)
    return content
