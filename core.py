from txtapi import readtxt
from wordapi import readword, transdoc
from pptapi import readppt, transppt
from pdfapi import readpdf
import utils
import config
from model import FileInfo
from typing import List
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN,SpectralClustering
from sklearn import metrics


def transform(fpath, tdir, extname):
    if extname == '.doc':
        transdoc.doc2docx(fpath, tdir, remove=False)
        return True
    if extname == '.ppt':
        transppt.ppt2pptx(fpath, tdir, remove=False)
        return True
    return False


def analysis(fpath, extname):
    content = None
    kw = []
    farr = []

    # do extract below
    if extname == '.txt':
        content = readtxt.read(fpath)

    if extname == '.docx':
        content = readword.readtxt(fpath)
    if extname == '.doc':
        content = readword.readtxt(fpath + 'x')

    if extname == '.pptx':
        content = readppt.readtxt(fpath)
    if extname == '.ppt':
        content = readppt.readtxt(fpath + 'x')

    if extname == '.pdf':
        content = readpdf.readtext(fpath)

    # do analysis
    if content is not None:
        kw = utils.get_keywords(content, config.kw_topk)
        freq = utils.get_freq(content)
        farr = list(map(lambda x: str(freq[x]) if x in freq else 0, kw))

    return ','.join(kw), ','.join(farr)


def file_cluster(fobjs: List[FileInfo]):
    words = {}
    for fobj in fobjs:
        for kw, freq in zip(fobj.keywords, fobj.kwfreq):
            if kw in words:
                words[kw] += freq
            else:
                words[kw] = freq

    # make keyword score vec
    all_wordvec = []
    for fobj in fobjs:
        fobj.set_wordvec(words)
        all_wordvec.append(fobj.wordvec)

    # pca
    pca = PCA(n_components=20)
    fprints = pca.fit_transform(all_wordvec)
    print(pca.explained_variance_ratio_)
    # fprints = all_wordvec

    # do cluster
    # kmeans
    # cluster_model = KMeans(n_clusters=6, random_state=1).fit(fprints)
    # labels = cluster_model.labels_
    # sc = metrics.silhouette_score(fprints, labels, metric='euclidean')

    # dbscan
    # cluster_model = DBSCAN(eps=1,  # 邻域半径
    #                        min_samples=2,  # 最小样本点数，MinPts
    #                        metric='euclidean',
    #                        metric_params=None,
    #                        algorithm='auto',  # 'auto','ball_tree','kd_tree','brute'
    #                        # leaf_size=30,  # balltree,cdtree的参数
    #                        p=None,  #
    #                        n_jobs=1).fit(fprints)
    # labels = cluster_model.labels_

    # spectral
    cluster_model = SpectralClustering(n_clusters=5, gamma=0.1).fit(fprints)
    labels = cluster_model.labels_

    return labels
