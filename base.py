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

def inc(dict, key):
    dict.setdefault(key, 0)
    dict[key] += 1

def getPattern(passwd, digitals, chars, specials):
    pattern = ""
    lstType = "S" # magic begin
    lstPos = -1
    # curTpype = ""
    n = len(passwd)
    for i in range(n):
        letter = passwd[i : i + 1]
        if bytes.isdigit(letter):
            curType = "D"
        elif bytes.isalpha(letter):
            curType = "A"
        else:
            curType = "N"
        if curType != lstType:
            if lstType != "S":
                pattern += lstType + str(i - lstPos) + " "
                sequence = passwd[lstPos : i]
                if lstType == "D":
                    inc(digitals, sequence)
                elif lstType == "A":
                    inc(chars, sequence)
                else:
                    inc(specials, sequence)
            lstPos = i

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

def printRank(dict, type, prefix):
    outf = open(prefix + "-%s.txt" % type, "w")
    outf.write("different %s: %d\n\n" % (type, len(dict)))
    outf.write("<%s> <times>\n" % type)
    outf.write("-" * 40 + "\n")
    for key, value in dict:
        outf.write("%s %d\n" % (key, value))
    outf.close()

def printPinyinPasswd(passwds, userNums, prefix):
    outf = open(prefix + "-pinyinPasswords.txt", "w")
    outf.write("%d/%d use pinyin in password\n\n" % (len(passwds), userNums))
    outf.write("-" * 40 + "\n")
    for item in passwds:
        outf.write("%s\n" % item)
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
                inc(words, word)
            continue

        tokens, succ = pyt.scan(word)
        if succ and (len(tokens) > 1):
            flag = True
            inc(pinyins, word)
    return flag

def useEmail(passwd, email):
    return passwd == email

def useId(passwd, id):
    return passwd == id

class Base(object, metaclass=ABCMeta):
    WORDS = [x.lower() for x in words.words("en")]
    NAMES = [x.lower() for x in (names.words("male.txt") + names.words("female.txt"))]
    def __init__(self, id, inputfile):
        self.id = id
        inf = open(inputfile, "rb")
        self.lines = inf.readlines()
        inf.close()

        self.pyt = PyTrie()
        self.pyt.setup()

        self.passwds = {}


    @abstractmethod
    def getPasswd(self, line):
        pass

    @abstractmethod
    def getFullEmail(self, line):
        pass

    def getEmail(self, line):
        return self.getFullEmail(line).split(b"@")[0]

    def getEmailType(self, line):
        emailAndType = self.getFullEmail(line).split(b"@")
        if len(emailAndType) <= 1:
            return b""
        else:
            return emailAndType[1]

    @abstractmethod
    def getId(self, line):
        pass

    '''
        1. calculate different passwords,   and save to "YaHoo/CSDN-passwords.txt"
        2. calculate password patterns,     and save to "YaHoo/CSDN-patterns.txt"
        3. calculate digital sequences,     and save to "YaHoo/CSDN-digits.txt"
        4. calculate character sequences,   and save to "YaHoo/CSDN-characters.txt"
        5. calculate other sequences,       and save to "YaHoo/CSDD-specials.txt"
        6. caluclate diffent email types,   and save to "YaHoo/CSDN-emails.txt"
    '''
    def analyzeComponent(self):
        passwds = {}

        patterns = {}

        digitals = {}
        chars = {}
        specials = {}

        emails = {}

        n = len(self.lines)
        for idx, line in enumerate(self.lines):
            passwd = self.getPasswd(line)
            inc(passwds, passwd)

            email = self.getEmailType(line)
            inc(emails, email)

            pattern = getPattern(passwd, digitals, chars, specials)
            inc(patterns, pattern)

            if idx % ECHO == 0:
                sys.stdout.write("\rprocessed %d/%d" % (idx, n))
                sys.stdout.flush()
                time.sleep(0.1)

        passwds = sortByValue(passwds)
        printRank(passwds, "passwords",self.id)

        patterns = sortByValue(patterns)
        printPatterns(patterns, self.id)

        digitals = sortByValue(digitals)
        printRank(digitals, "digits",self.id)

        chars = sortByValue(chars)
        printRank(chars, "chars", self.id)

        specials = sortByValue(specials)
        printRank(specials, "specials", self.id)

        emails = sortByValue(emails)
        printRank(emails, "emails", self.id)

    '''
        1. calculate different pinyins,     and save to "YaHoo/CSDN-pinyins.txt"
        2. calculate different words,       and save to "YaHoo/CSDN-words.txt"
    '''
    def analyzePinyin(self):
        pinyinPasswd = set([])
        pinyins = {}
        words = {}
        n = len(self.lines)
        for idx, line in enumerate(self.lines):
            passwd = self.getPasswd(line)

            if usePinyinOrWord(passwd, self.pyt, pinyins, words, \
                               Base.WORDS, Base.NAMES):
                pinyinPasswd.add(line[:-2])

            if idx % ECHO == 0:
                sys.stdout.write("\rprocessed %d/%d" % (idx, n))
                sys.stdout.flush()
                time.sleep(0.1)

        pinyins = sortByValue(pinyins)
        printRank(pinyins, "pinyins", self.id)

        words = sortByValue(words)
        printRank(words, "words", self.id)

        printPinyinPasswd(pinyinPasswd, len(self.lines), self.id)

    '''
        1. calculate how many password are the same as id or email, 
            and save to "YaHoo/relations.txt"
    '''
    def analyzeRelation(self):
        emailCount = 0
        idCount = 0
        n = len(self.lines)
        for idx, line in enumerate(self.lines):
            passwd = self.getPasswd(line)
            email = self.getEmail(line)
            id = self.getId(line)

            if useEmail(passwd, email):
                emailCount += 1
            if useId(passwd, id):
                idCount += 1

            if idx % ECHO == 0:
                sys.stdout.write("\rprocessed %d/%d" % (idx, n))
                sys.stdout.flush()
                time.sleep(0.1)

            outf = open(self.id + "-relations.txt", "w")
            outf.write("%d/%d use email as password\n" % (emailCount, n))
            outf.write("%d/%d use id as password\n" % (idCount, n))
            outf.close()
