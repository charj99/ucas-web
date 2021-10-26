import re
from nltk.corpus import names, words

INPUTFILE_YAHOO = "plaintxt_yahoo.txt"
INPUTFILE_CSDN = "www.csdn.net.sql"

SEPERATOR_YAHOO = b":"
SEPERATOR_CSDN = b" # "

WORDS = words.words("en")
NAMES = names.words("male.txt") + names.words("female.txt")
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

def printPinyin(pinyin, userNums, prefix):
    outf = open(prefix + "-pinyin.txt", "w")
    outf.write("%d/%d use pinyin in password\n\n" % (len(pinyin), userNums))
    outf.write("-" * 40 + "\n")
    for item in pinyin:
        outf.write("%s\n" % item)
    outf.close()

def useSingleWord(word):
    s = bytes.decode(word).lower()
    return s in WORDS

def useName(word):
    s = bytes.decode(word).lower()
    return s in NAMES

def usePinyin(passwd, pyt):
    flag = False

    # get word part of passwd
    words = re.findall(rb"[a-z]+", passwd, re.I)
    for word in words:
        tokens, succ = pyt.scan(word)
        if succ:
            succ &= (not useSingleWord(word))
        if succ:
            succ &= (not useName(word))
        flag |= succ
    return flag
