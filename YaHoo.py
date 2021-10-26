from utils import *
class YaHoo(object):
    def __init__(self):
        inf = open(INPUTFILE_YAHOO, "r")
        self.lines = inf.readlines()
        inf.close()
        self.patterns = {}
        self.nChars = {} # unkown characters used in passwd
        self.id = "YaHoo"

    def analyzeComponent(self):
        self.patterns.clear()
        self.nChars.clear()
        for line in self.lines:
            tuple = line[:-1].split(":")
            passwd = tuple[-1]
            pattern = getPattern(passwd, self.nChars)
            self.patterns.setdefault(pattern, 0)
            self.patterns[pattern] += 1

        self.patterns = sortByValue(self.patterns)
        printPatterns(self.patterns, self.id)

        self.nChars = sortByValue(self.nChars)
        printNChars(self.nChars, self.id)
