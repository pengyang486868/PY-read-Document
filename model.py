import math


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
