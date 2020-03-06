from txtapi import readtxt
from wordapi import readword, transdoc
from pptapi import readppt, transppt
from pdfapi import readpdf
import utils
import config
import uuid
import numpy as np
from model import FileInfo
from typing import List
from sklearn.cluster import KMeans, DBSCAN, SpectralClustering
from sklearn import metrics
from sklearn.decomposition import PCA
import torch
from torch.utils.data import TensorDataset, DataLoader
import torch.optim as optim
import torch.nn as nn
from model import MLP


def transform(fpath, tdir, extname):
    if extname == '.doc':
        transdoc.doc2docx(fpath, tdir, remove=False)
        return True
    if extname == '.ppt':
        transppt.ppt2pptx(fpath, tdir, remove=False)
        return True
    return False


def analysis(fpath, extname, imgdir):
    content = None
    images = []

    kw_arr = []
    freq_arr = []
    ph_arr = []
    nw_arr = []
    sum_arr = []

    # do extract below
    if extname == '.txt':
        content = readtxt.read(fpath)

    if extname == '.docx':
        content = readword.readtxt(fpath)
    if extname == '.doc':
        content = readword.readtxt(fpath + 'x')

    if extname == '.pptx':
        content = readppt.readtxt(fpath)
        images = readppt.readimg(fpath, imgdir, str(uuid.uuid4()))
    if extname == '.ppt':
        content = readppt.readtxt(fpath + 'x')
        images = readppt.readimg(fpath + 'x', imgdir, str(uuid.uuid4()))

    if extname == '.pdf':
        content = readpdf.readtext(fpath)

    # do analysis
    if content is not None:
        # key words
        kw_arr = utils.get_keywords(content, config.kw_topk)
        # frequency array
        freq = utils.get_freq(content)
        freq_arr = list(map(lambda x: str(freq[x]) if x in freq else 0, kw_arr))
        # key phrases
        ph_arr = utils.get_phrase(content, n=10)
        # new words
        nw_arr = utils.get_newwords(content, n=20)
        # auto summary
        sum_arr = utils.get_summary(content, n=5)

    # give keywords to images
    # ['fname', 'keywords', 'relatedtxt']
    for cimg in images:
        cimg['keywords'] = ','.join(utils.get_keywords([cimg['relatedtxt']], config.kw_topk_image))

    return (','.join(kw_arr), ','.join(freq_arr),
            ','.join(ph_arr), ','.join(nw_arr), ','.join(sum_arr),
            images
            )


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

    # pca make fingerprints
    pca = PCA(n_components=20)
    fprints = pca.fit_transform(all_wordvec)
    print('PCA ratio sum:', sum(pca.explained_variance_ratio_))
    print()
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


def file_classify_demo(fobjs: List[FileInfo]):
    words = {}
    for fobj in filter(lambda x: not x.istest, fobjs):
        for kw, freq in zip(fobj.keywords, fobj.kwfreq):
            if kw in words:
                words[kw] += freq
            else:
                words[kw] = freq

    # make keyword score vec: train and test
    all_wordvec = []
    all_wordvec_test = []
    labels = []
    for fobj in fobjs:
        fobj.set_wordvec(words)
        if not fobj.istest:
            all_wordvec.append(fobj.wordvec)
            labels.append(fobj.label)
            # curlabel = [0] * 5
            # curlabel[fobj.label] = 1
            # labels.append(curlabel)
        else:
            all_wordvec_test.append(fobj.wordvec)

    # pca make fingerprints
    pca = PCA(n_components=20)
    pca.fit(all_wordvec)
    fprints = pca.transform(all_wordvec)
    fprints_test = pca.transform(all_wordvec_test)
    print('PCA ratio sum:', sum(pca.explained_variance_ratio_))
    print()

    x_train = torch.from_numpy(fprints).float()
    x_test = torch.from_numpy(fprints_test).float()
    y_train = torch.Tensor(labels).long()  # float()

    train_dataset = TensorDataset(x_train, y_train)
    dloader = DataLoader(train_dataset, batch_size=6, shuffle=True)

    model = MLP()
    optimizer = optim.Adam(model.parameters(), lr=0.05)
    lossfunc = nn.CrossEntropyLoss()

    epoch = 50
    for ecnt in range(epoch):
        print('Epoch:', ecnt)
        for i, data in enumerate(dloader):
            optimizer.zero_grad()
            inputs, labels = data
            inputs = torch.autograd.Variable(inputs)
            labels = torch.autograd.Variable(labels)

            outputs = model(inputs)
            loss = lossfunc(outputs, labels)  # / outputs.size()[0]
            # loss = torch.Tensor([0])
            # for b in range(outputs.size()[0]):
            #     loss += sum(abs(outputs[b] - labels[b]))
            # loss /= outputs.size()[0]

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5)
            optimizer.step()

            # if i % 1 == 0:
            #     print(i, ":", loss)
            #     print(outputs)
            #     print(labels)

        # y_train_step = model(x_train)
        # y_train_step_label = np.argmax(y_train_step.data)

    y_train_look = model(x_train)
    y_test = model(x_test)
    print(y_train_look)
    print(y_test)
