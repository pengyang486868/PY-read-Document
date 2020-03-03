import math
import torch.nn as nn
import torch.nn.functional as F


class FileInfoBase():
    def __init__(self):
        self.id = 0
        self.fname = ''
        self.extname = ''
        self.username = ''


class FileInfo(FileInfoBase):
    def __init__(self):
        super().__init__()
        self.keywords = []
        self.kwfreq = []
        self.istest = False
        self.label = 0
        self.wordvec = []
        self.fingerprint = []

    def __str__(self):
        return self.fname

    def set_wordvec(self, worddic: dict):
        ftotal = sum(self.kwfreq)
        alltotal = sum(worddic.values())
        for key in worddic.keys():
            found = False
            for kw, freq in zip(self.keywords, self.kwfreq):
                if kw == key:
                    found = True
                    self.wordvec.append(self.tfidf(freq, ftotal, alltotal))
                    break
            if not found:
                self.wordvec.append(0)

    @staticmethod
    def tfidf(freq, flen, allwords):
        return freq / flen * math.log(allwords / freq)


class MLP(nn.Module):
    def __init__(self):
        super(MLP, self).__init__()
        self.fc1 = nn.Linear(20, 5)
        # self.fc2 = nn.Linear(5, 5)

    def forward(self, din):
        # din = din.view(-1, 28 * 28)
        h1 = F.relu(self.fc1(din))
        # dout = F.relu(self.fc2(h1))
        return h1  # F.softmax(dout)
