from utils import *
from trie import *
import time, sys

class YaHoo(object):
    def __init__(self):
        self.id = "YaHoo"
        inf = open(INPUTFILE_YAHOO, "rb")
        self.lines = inf.readlines()
        inf.close()

        self.patterns = {}
        self.nChars = {} # unkown characters used in passwd

        self.pinyin = set([])
        self.pyt = PyTrie()
        self.pyt.setup()

    def getPasswd(self, line):
        return line[:-2].split(SEPERATOR_YAHOO)[-1]

    def analyzeComponent(self):
        self.patterns.clear()
        self.nChars.clear()

        n = len(self.lines)
        for idx, line in enumerate(self.lines):
            passwd = self.getPasswd(line)
            pattern = getPattern(passwd, self.nChars)

            self.patterns.setdefault(pattern, 0)
            self.patterns[pattern] += 1

            if idx % ECHO == 0:
                sys.stdout.write("\rprocessed %d/%d" % (idx, n))
                sys.stdout.flush()
                time.sleep(0.1)

        self.patterns = sortByValue(self.patterns)
        printPatterns(self.patterns, self.id)

        self.nChars = sortByValue(self.nChars)
        printNChars(self.nChars, self.id)

    def analyzePinyin(self):
        self.pinyin.clear()
        n = len(self.lines)
        for idx, line in enumerate(self.lines):
            passwd = self.getPasswd(line)

            if usePinyin(passwd, self.pyt):
                self.pinyin.add(line[:-2])

            if idx % ECHO == 0:
                sys.stdout.write("\rprocessed %d/%d" % (idx, n))
                sys.stdout.flush()
                time.sleep(0.1)

        printPinyin(self.pinyin, len(self.lines), self.id)