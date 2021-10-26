from utils import *
class CSDN(object):
    def __init__(self):
        inf = open(INPUTFILE_CSDN, "r", encoding="unicode-esacpe")
        self.lines = inf.readlines()
        inf.close()
        self.patterns = {}
        self.nChars = {} # unkown characters used in passwd
        self.id = "CSDN"

    def analyzeComponent(self):
        self.patterns.clear()
        self.nChars.clear()
        for line in self.lines:
            tuple = line[:-1].split(" # ")
            passwd = tuple[1]
            pattern = getPattern(passwd, self.nChars)
            self.patterns.setdefault(pattern, 0)
            self.patterns[pattern] += 1

        self.patterns = sortByValue(self.patterns)
        printPatterns(self.patterns, self.id)

        self.nChars = sortByValue(self.nChars)
        printNChars(self.nChars, self.id)