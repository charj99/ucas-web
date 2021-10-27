import re
from abc import ABCMeta, abstractmethod
import sys, time
from trie import PyTrie
from nltk.corpus import words, names

INPUTFILE_YAHOO = "plaintxt_yahoo.txt"
INPUTFILE_CSDN = "www.csdn.net.sql"

SEPERATOR_YAHOO = b":"
SEPERATOR_CSDN = b" # "

ECHO = 1000

def getPattern(passwd, nChrDict):
    pattern = ""
    lstType = "S" # magic begin
    curTpype = ""
    n = len(passwd)
    for i in range(n):
        letter = passwd[i : i + 1]
        if bytes.isdigit(letter):
            curType = "D"
        elif bytes.isalpha(letter):
            curType = "A"
        else:
            curType = "N"
            nChrDict.setdefault(letter, 0)
            nChrDict[letter] += 1
        if curType != lstType:
            pattern += curType
        lstType = curType

    # if "N" in pattern:
    #    print(passwd)
    return pattern

def sortByValue(dict):
    return sorted(dict.items(), key=lambda x: x[1], reverse=True)

def printPatterns(patterns, prefix):
    outf = open(prefix + "-patterns.txt", "w")
    outf.write("different pattern numbers: %d\n" % len(patterns))
    outf.write("D: digits, A: alphabets, N: unknown\n\n")
    outf.write("<pattern> <times>\n")
    outf.write("-" * 40 + "\n")
    for key, value in patterns:
        outf.write("%s %d\n" % (key, value))
    outf.close()

def printNChars(nChars, prefix):
    outf = open(prefix + "-unknowCharacters.txt", "w")
    outf.write("different unknow characters: %d\n\n" % len(nChars))
    outf.write("<character> <times>\n")
    outf.write("-" * 40 + "\n")
    for key, value in nChars:
        outf.write("%s %d\n" % (key, value))
    outf.close()

def printPinyinPasswd(passwds, userNums, prefix):
    outf = open(prefix + "-pinyinPasswords.txt", "w")
    outf.write("%d/%d use pinyin in password\n\n" % (len(passwds), userNums))
    outf.write("-" * 40 + "\n")
    for item in passwds:
        outf.write("%s\n" % item)
    outf.close()

def printPinyinOrWords(pinWords, type, prefix):
    outf = open(prefix + "-%s.txt" % type, "w")
    outf.write("different %s: %d\n\n" % (type, len(pinWords)))
    outf.write("-" * 40 + "\n")
    for key, value in pinWords:
        outf.write("%s %d\n" % (key, value))
    outf.close()

def useSingleWord(word, WORDS):
    s = bytes.decode(word).lower()
    return s in WORDS

def useName(word, NAMES):
    s = bytes.decode(word).lower()
    return s in NAMES

def usePinyinOrWord(passwd, pyt, pinyins, words, WORDS, NAMES):
    flag = False

    # get word part of passwd
    wordsInPasswd = re.findall(rb"[a-z]+", passwd, re.I)
    for word in wordsInPasswd:
        if useSingleWord(word, WORDS) or useName(word, NAMES):
            if len(word) > 1:
                words.setdefault(word, 0)
                words[word] += 1
            continue

        tokens, succ = pyt.scan(word)
        if succ and (len(tokens) > 1):
            flag = True
            pinyins.setdefault(word, 0)
            pinyins[word] += 1
    return flag


class Base(object, metaclass=ABCMeta):
    WORDS = [x.lower() for x in words.words("en")]
    NAMES = [x.lower() for x in (names.words("male.txt") + names.words("female.txt"))]
    def __init__(self, id, inputfile):
        self.id = id
        inf = open(inputfile, "rb")
        self.lines = inf.readlines()
        inf.close()

        self.patterns = {}
        self.nChars = {}  # unkown characters used in passwd

        self.pinyinPasswd = set([])
        self.pyt = PyTrie()
        self.pyt.setup()
        self.pinyins = {}
        self.words = {}

    @abstractmethod
    def getPasswd(self, line):
        pass

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
        self.pinyinPasswd.clear()
        self.pinyins.clear()
        self.words.clear()
        n = len(self.lines)
        for idx, line in enumerate(self.lines):
            passwd = self.getPasswd(line)

            if usePinyinOrWord(passwd, self.pyt, self.pinyins, self.words, \
                               Base.WORDS, Base.NAMES):
                self.pinyinPasswd.add(line[:-2])

            if idx % ECHO == 0:
                sys.stdout.write("\rprocessed %d/%d" % (idx, n))
                sys.stdout.flush()
                time.sleep(0.1)

        self.pinyins = sortByValue(self.pinyins)
        printPinyinOrWords(self.pinyins, "pinyins", self.id)

        self.words = sortByValue(self.words)
        printPinyinOrWords(self.words, "words", self.id)

        printPinyinPasswd(self.pinyinPasswd, len(self.lines), self.id)

