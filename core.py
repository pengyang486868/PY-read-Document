from txtapi import readtxt
from wordapi import readword, transdoc
from pptapi import readppt, transppt
from pdfapi import readpdf
from dwgapi import readdxf
import utils
import config
import uuid
import numpy as np
from model import FileInfo, ImageInfo
from typing import List
from sklearn.cluster import KMeans, DBSCAN, SpectralClustering
from sklearn import metrics
from sklearn.decomposition import PCA
import torch
from torch.utils.data import TensorDataset, DataLoader
import torch.optim as optim
import torch.nn as nn
from networks import MLP
from model import NormalSearchResult, NaturalSearchResult
import math
from datetime import datetime


# transform file format
def transform(fpath, tdir, extname):
    if extname == '.doc':
        transdoc.doc2docx(fpath, tdir, remove=False)
        return True
    if extname == '.ppt':
        transppt.ppt2pptx(fpath, tdir, remove=False)
        return True
    if extname == '.dwg':
        return True
    return False


# analysis file to structure data
def analysis(fpath, extname, imgdir):
    content = None
    images = []
    drawings = []

    kw_arr = []
    freq_arr = []
    ph_arr = []
    nw_arr = []
    sum_arr = []

    # do extract below
    # if extname == '.txt':
    #     content = readtxt.read(fpath)
    #
    # if extname == '.docx':
    #     content = readword.readtxt(fpath)
    #     images = readword.readimg(fpath, imgdir, str(uuid.uuid4()))
    # if extname == '.doc':
    #     content = readword.readtxt(fpath + 'x')
    #     images = readword.readimg(fpath + 'x', imgdir, str(uuid.uuid4()))
    #
    # if extname == '.pptx':
    #     content = readppt.readtxt(fpath)
    #     images = readppt.readimg(fpath, imgdir, str(uuid.uuid4()))
    # if extname == '.ppt':
    #     content = readppt.readtxt(fpath + 'x')
    #     images = readppt.readimg(fpath + 'x', imgdir, str(uuid.uuid4()))
    #
    # if extname == '.pdf':
    #     content = readpdf.readtext(fpath)

    if extname == '.dxf':
        content = readdxf.readtxt(fpath)
        drawings = readdxf.split_drawing_byblock(fpath)

    # do analysis
    # if content is not None:
    #     # key words
    #     kw_arr = utils.get_keywords(content, config.kw_topk)
    #     # word frequency array
    #     freq = utils.get_freq(content)
    #     freq_arr = list(map(lambda x: str(freq[x]) if x in freq else 0, kw_arr))
    #     # key phrases
    #     ph_arr = utils.get_phrase(content, n=10)
    #     # new words
    #     nw_arr = utils.get_newwords(content, n=20)
    #     # auto summary
    #     sum_arr = utils.get_summary(content, n=5)

    # give keywords to images
    # ['fname', 'keywords', 'relatedtxt']
    makeparam = {}
    for cimg in images:
        # cimg['keywords'] = ','.join(utils.get_keywords([cimg['relatedtxt']], config.kw_topk_image))
        makeparam[cimg['fname']] = cimg['relatedtxt']

    # kwdic = utils.get_keywordsmany(makeparam, config.kw_topk_image)
    # for cimg in images:
    #     cimg['keywords'] = ','.join(kwdic[cimg['fname']][0])
    #     cimg['newwords'] = ','.join(kwdic[cimg['fname']][1])
    #     cimg['docname'] = fpath

    return (','.join(kw_arr), ','.join(freq_arr),
            ','.join(ph_arr), ','.join(nw_arr), ','.join(sum_arr),
            images, drawings
            )


# clustering
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
    # cluster_model = KMeans(n_clusters=3, random_state=1).fit(fprints)
    # labels = cluster_model.labels_
    # sc = metrics.silhouette_score(fprints, labels, metric='euclidean')

    # dbscan
    # cluster_model = DBSCAN(eps=1.2,  # 邻域半径
    #                        min_samples=2,  # 最小样本点数，MinPts
    #                        metric='euclidean',
    #                        metric_params=None,
    #                        algorithm='auto',  # 'auto','ball_tree','kd_tree','brute'
    #                        # leaf_size=30,  # balltree,cdtree的参数
    #                        p=None,  #
    #                        n_jobs=1).fit(fprints)
    # labels = cluster_model.labels_

    # spectral
    cluster_model = SpectralClustering(n_clusters=3, gamma=0.1).fit(fprints)
    labels = cluster_model.labels_

    print(labels)

    utils.plotxy(fprints[:, 0], fprints[:, 1], fprints[:, 2], labels)

    return labels


# demo for AI classify: train and output
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
            torch.nn.utils.clip_grad_norm_(model.parameters(), 5)  # clip param important
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


# basic search by word
def search_basic(inputword, fobjs: List[FileInfo], givetime=True):
    start = datetime.now()
    nfile = len(fobjs)
    words = {}
    for fobj in fobjs:
        for kw, freq in zip(fobj.keywords, fobj.kwfreq):
            if kw in words:
                words[kw] += freq
            else:
                words[kw] = freq

    # swords = utils.get_keywords(word, 10)
    swords = inputword.split(' ')
    result = []
    for fo in fobjs:
        currentresult = NormalSearchResult()
        currentresult.fpath = fo.fname
        currentresult.sword = inputword
        flen_param = 1 / math.log(sum(fo.kwfreq), 2)
        phlenparam = 1 / len(fo.phrase)
        nwlenparam = 1 / len(fo.newwords)

        score_keyword = 0
        score_phrase = 0
        score_namedentity = 0
        beta_p = 2.0
        beta_n = 4.0
        for sw in swords:
            # match keywords
            for indx, (w, fw) in enumerate(zip(fo.keywords, fo.kwfreq)):
                if w == sw:
                    score_keyword += nfile * fw / words[w] * flen_param * pow(2, (-1 * indx / 10))

            # match phrase
            for ph in fo.phrase:
                score_phrase += phlenparam * beta_p * utils.str_similar(sw, ph)

            # match named entities
            for ne in fo.newwords:
                score_namedentity += nwlenparam * beta_n * utils.str_similar(sw, ne)

        # make result
        currentresult.score = score_keyword + score_phrase + score_namedentity
        currentresult.scoredetail = (score_keyword, score_phrase, score_namedentity)
        result.append(currentresult)

    result = list(filter(lambda x: x.score > 0, result))
    result.sort(key=lambda x: x.score, reverse=True)
    totaltime = (datetime.now() - start).total_seconds()

    if not givetime:
        return result
    return result, totaltime


# natural language search
def search_natural(sentence, fobjs: List[FileInfo]):
    relwords = ['和', '或', '不', '的']  # 'and' is actually default
    pass


# search images normal
def search_img(inputword, imgobjs: List[ImageInfo], givetime=True):
    start = datetime.now()
    nword_min = 3

    swords = inputword.split(' ')
    result = []
    for fo in imgobjs:
        currentresult = NormalSearchResult()
        currentresult.fpath = fo.fname
        currentresult.sword = inputword
        currentresult.obj = fo

        score_keyword = 0
        score_namedentity = 0
        beta_k = 2.0
        beta_n = 4.0
        kwlenparam = 1 / max(nword_min, len(fo.keywords))
        nwlenparam = 1 / max(nword_min, len(fo.newwords))
        for sw in swords:
            # match keywords
            for indx, w in enumerate(fo.keywords):
                if w == sw:
                    score_keyword += kwlenparam * beta_k * utils.str_similar(sw, w)

            # match named entities
            for ne in fo.newwords:
                score_namedentity += nwlenparam * beta_n * utils.str_similar(sw, ne)

        # make result
        currentresult.score = score_keyword + score_namedentity
        currentresult.scoredetail = (score_keyword, score_namedentity)
        result.append(currentresult)

    result = list(filter(lambda x: x.score > 0, result))
    result.sort(key=lambda x: x.score, reverse=True)
    totaltime = (datetime.now() - start).total_seconds()

    if not givetime:
        return result
    return result, totaltime


# recommand simple
def recommand(thisfile: FileInfo, fobjs: List[FileInfo], rnum=10):
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
    pca.fit(all_wordvec)
    for fobj in fobjs:
        fobj.fingerprint = pca.transform([fobj.wordvec])[0]
    thisfile.fingerprint = pca.transform([thisfile.wordvec])[0]

    # find nearest
    distarr = []
    for fobj in fobjs:
        if fobj.id == thisfile.id and fobj.fname == thisfile.fname:
            continue
        d = np.linalg.norm(np.array(fobj.fingerprint) - np.array(thisfile.fingerprint))
        distarr.append({'file': fobj, 'dist': d})
    distarr.sort(key=lambda x: x['dist'])

    if len(distarr) < rnum:
        return distarr
    return distarr[0:rnum]
