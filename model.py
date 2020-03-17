import math


class FileInfoBase:
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
        self.phrase = []
        self.newwords = []
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


class ImageInfo:
    def __init__(self):
        self.id = 0
        self.fname = ''
        self.docname = ''
        self.keywords = []
        self.newwords = []


class SearchResultBase:
    def __init__(self):
        self.fpath = ''
        self.score = 0
        self.scoredetail = None
        self.obj = None

    def __str__(self):
        return self.fpath + ' | ' + str(self.score)


class NormalSearchResult(SearchResultBase):
    def __init__(self):
        super().__init__()
        self.sword = ''


class NaturalSearchResult(SearchResultBase):
    def __init__(self):
        super().__init__()
        self.sentence = ''
        self.words = []
        self.restrict = None
