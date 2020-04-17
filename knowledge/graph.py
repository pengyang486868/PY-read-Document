import math
from model import FileInfo
from typing import List
from functools import reduce
import numpy as np
from pyecharts.charts import Graph
from pyecharts.options.series_options import LineStyleOpts


def generate(fobjs: List[FileInfo]):
    words = tuple(y for y in set(reduce(lambda x, y: x + y, [x.keywords for x in fobjs])) if len(y) > 1)
    nodes = [{'name': x, 'symbolSize': np.random.rand() * 10 + 10, 'value': np.random.rand()} for x in words]
    links = []
    for i in nodes:
        for j in nodes:
            dice = np.random.rand()
            if dice > 0.997:
                links.append({"source": i['name'], "target": j['name']})
    # print(words)
    graph = Graph()
    graph.add("", nodes, links, repulsion=8000, layout='force', linestyle_opts=LineStyleOpts(curve=0.3))
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
    graph.add("", nodes, links, repulsion=8000, layout='force', linestyle_opts=LineStyleOpts(curve=0.3))
    # graph.show_config()
    graph.render(path="./chart1.html")
