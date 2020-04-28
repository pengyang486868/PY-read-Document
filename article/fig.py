from docDAL import mysql as conn
from model import FileInfo
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np

plt.rc('font', family='Times New Roman')


def pca_fig():
    fobjs = conn.get_file_info(returnobj=True)
    words = FileInfo.allwordsdic(fobjs)

    # make keyword score vec
    all_wordvec = []
    for fobj in fobjs:
        fobj.set_wordvec(words)
        all_wordvec.append(fobj.wordvec)

    # pca make fingerprints
    n = 30
    pca = PCA(n_components=n)
    fprints = pca.fit_transform(all_wordvec)
    print('PCA ratio sum:', sum(pca.explained_variance_ratio_))

    fig, ax1 = plt.subplots()

    ax1.bar(range(n), pca.explained_variance_ratio_)
    ax2 = ax1.twinx()
    ax2.plot(range(n), np.cumsum(pca.explained_variance_ratio_), c='r')
    ax1.vlines(x=23, ymin=0, ymax=0.15, linestyles=':')
    ax2.hlines(y=0.8, xmin=10, xmax=30, linestyles=':', lw=3)
    ax2.grid()
    plt.show()


def cluster_result():
    n = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    sc = [0.191, 0.168, 0.181, 0.218, 0.229, 0.243, 0.229, 0.229, 0.227]
    cal = [10.06, 8.96, 8.32, 8.26, 8, 7.39, 6.87, 6.93, 6.91]

    fig, ax1 = plt.subplots()

    name1 = 'Silhouette coefficient'
    line1 = ax1.plot(n, sc, '-o', c='k', label=name1, ms=10, markerfacecolor='w')
    # ax1.scatter(n, sc, c='w', label=name1, marker='o', s=80, edgecolor='b')
    plt.ylim(0.16, 0.25)
    plt.ylabel(name1)
    plt.xlabel('Cluster amount $k$')
    ax1.xaxis.grid()

    name2 = 'Calinski-Harabasz score'
    ax2 = ax1.twinx()
    line2 = ax2.plot(n, cal, '--^', c='k', label=name2, ms=10)
    # ax2.scatter(n, cal, c='w', label=name2, marker='^', s=80, edgecolor='r')
    plt.ylabel(name2)
    plt.ylim(5, 10.5)
    plt.legend(line1 + line2, [name1, name2], shadow=True, fancybox=True, loc='lower right',
               bbox_to_anchor=(0.95, 0.05))

    plt.show()


if __name__ == '__main__':
    cluster_result()
