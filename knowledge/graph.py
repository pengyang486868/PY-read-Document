import math
from model import FileInfo
from typing import List
from functools import reduce
import numpy as np
from pyecharts.charts import Graph
from pyecharts.options.series_options import LineStyleOpts
from sklearn.decomposition import PCA


def generate(fobjs: List[FileInfo]):
    # words = tuple(y for y in set(reduce(lambda x, y: x + y, [x.keywords for x in fobjs])) if len(y) > 1)
    words = FileInfo.allwordsdic(fobjs, minlen=2)
    all_wordvec = []
    for fobj in fobjs:
        fobj.set_wordvec(words)
        all_wordvec.append(fobj.wordvec)

    # pca make fingerprints
    pca = PCA(n_components=20)
    fprints = pca.fit_transform(all_wordvec)

    # dist = []
    # for i in range(len(fprints)):
    #     dist.append(np.linalg.norm(fprints[0] - fprints[i]))

    words_arr = list(words.keys())
    nw = len(words_arr)
    n = len(fobjs)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j] = 1 / np.linalg.norm(fprints[i] - fprints[j])

    maxfreq = max(words.values())

    linkmatrix = np.zeros((nw, nw))
    for i in range(nw):
        for j in range(i + 1, nw):
            intersect = []
            for indx, fo in enumerate(fobjs):
                if words_arr[i] in fo.keywords and words_arr[j] in fo.keywords:
                    intersect.append(indx)
            linkmatrix[i][j] = sum([matrix[a][b] for a in intersect for b in intersect])

    nodes = []
    links = []
    tol = 0
    maxlink = 200
    linkvalues = [linkmatrix[i][j] for i in range(nw) for j in range(nw) if linkmatrix[i][j] > 0]
    maxvalue = max(linkvalues)
    if len(linkvalues) > maxlink:
        tol = sorted(linkvalues, reverse=True)[maxlink]

    for i in range(nw):
        for j in range(i + 1, nw):
            if linkmatrix[i][j] < tol:
                continue

            if words_arr[i] not in [node['name'] for node in nodes]:
                cnt = words[words_arr[i]]
                cursize = 30 * max(0.2, math.sqrt(cnt / maxfreq))
                nodes.append({'name': words_arr[i], 'symbolSize': cursize, 'value': cnt})
            if words_arr[j] not in [node['name'] for node in nodes]:
                cnt = words[words_arr[j]]
                cursize = 30 * max(0.2, math.sqrt(cnt / maxfreq))
                nodes.append({'name': words_arr[j], 'symbolSize': cursize, 'value': cnt})

            start = words[words_arr[i]]
            end = words[words_arr[j]]
            linestyle = {'width': 20.0 * max(0.05, linkmatrix[i][j] / maxvalue)}
            if start > end:
                links.append({"source": words_arr[i], "target": words_arr[j], 'lineStyle': linestyle})
            else:
                links.append({"source": words_arr[j], "target": words_arr[i], 'lineStyle': linestyle})

    graph = Graph()
    graph.add("", nodes, links, repulsion=1000, gravity=0.1, layout='force', linestyle_opts=LineStyleOpts(curve=0.1))
    # graph.show_config()
    graph.render(path="./chart1.html")
    return None


def chart_test():
    nodes = [{"name": "结点1", "symbolSize": 10}, {"name": "结点2", "symbolSize": 20}, {"name": "结点3", "symbolSize": 30},
             {"name": "结点4", "symbolSize": 40}, {"name": "结点5", "symbolSize": 50}, {"name": "结点6", "symbolSize": 40},
             {"name": "结点7", "symbolSize": 30}, {"name": "结点8", "symbolSize": 20}]
    links = []
    for i in nodes:
        for j in nodes:
            dice = np.random.rand()
            if dice > 0.6:
                links.append({"source": i['name'], "target": j['name']})

    # print(links)
    # print(nodes)
    graph = Graph()
    graph.add("", nodes, links, repulsion=8000, layout='force', linestyle_opts=LineStyleOpts(curve=0.1))
    # graph.show_config()
    graph.render(path="./chart1.html")
