from utils import *
class YaHoo(object):
    def __init__(self):
        inf = open(INPUTFILE_YAHOO, "rb")
        self.lines = inf.readlines()
        inf.close()
        self.patterns = {}
        self.nChars = {} # unkown characters used in passwd


    def analyzeComponent(self):
        self.patterns.clear()
        self.nChars.clear()
        for line in self.lines:
            tuple = line[:-2].split(b":")
            passwd = tuple[-1]
            pattern = getPattern(passwd, self.nChars)
            self.patterns.setdefault(pattern, 0)
            self.patterns[pattern] += 1

        self.patterns = sortByValue(self.patterns)
        printPatterns(self.patterns, "YaHoo")

        self.nChars = sortByValue(self.nChars)
        printNChars(self.nChars, "YaHoo")
