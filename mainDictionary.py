import sys, getopt

BASE_DIR = "./results/"
LIMIT_PASSWORD_YAHOO = 10
LIMIT_PATTERN_YAHOO = 100
LIMIT_DIGIT_YAHOO = 50
LIMIT_CHAR_YAHOO  = 50
LIMIT_SPECIAL_YAHOO  = 10
LIMIT_TIME_YAHOO = 1000000

LIMIT_PASSWORD_CSDN = 10
LIMIT_PATTERN_CSDN = 10
LIMIT_DIGIT_CSDN = 50
LIMIT_CHAR_CSDN  = 50
LIMIT_SPECIAL_CSDN  = 10
LIMIT_TIME_CSDN = 100000

DICT_NAME = "-dictionary.txt"

TYPE_DIGIT = "digits"
TYPE_CHAR = "chars"
TYPE_SPECIAL = "specials"

ECHO = 5

def getNum(line):
    return int(line.split(" ")[-1])


def getStr(line):
    return line.split(" ")[0][2 : -1]


def getCommonPasswords(prefix):
    inf = open(BASE_DIR + prefix + "-passwords.txt", "r")
    lines = inf.readlines()
    inf.close()
    begin = False

    if prefix == "YaHoo":
        LIMIT = LIMIT_PASSWORD_YAHOO
    else:
        LIMIT = LIMIT_PASSWORD_CSDN

    passwds = {}
    for i, line in enumerate(lines):
        line = line[:-1]
        if line == "-" * 40:
            begin = True
            continue

        if not begin:
            continue

        num = getNum(line)
        if num < LIMIT:
            print("get %d common passwords(used no less than %d times)" \
                  % (i + 1, LIMIT))
            return passwds

        s = getStr(line)
        passwds[s] = 1

    return passwds


def getPattern(line):
    return line.rsplit(" ", 1)[0]

def getP(list):
    sum = 0
    for item in list:
        sum += item[1]
    n = len(list)
    for i in range(n):
        list[i] = (list[i][0], list[i][1] / sum)
    return list


def readPatterns(prefix):
    inf = open(BASE_DIR + prefix + "-patterns.txt", "r")
    lines = inf.readlines()
    inf.close()

    if prefix == "YaHoo":
        LIMIT = LIMIT_PATTERN_YAHOO
    else:
        LIMIT = LIMIT_PATTERN_CSDN

    patterns = []

    begin = False
    for i, line in enumerate(lines):
        line = line[:-1]
        if line == "-" * 40:
            begin = True
            continue

        if not begin:
            continue

        num = getNum(line)
        if num < LIMIT:
            print("get %d patterns(used no less than %d times)" \
                  % (i + 1, LIMIT))
            return getP(patterns)

        pattern = getPattern(line)
        num = getNum(line)
        patterns.append((pattern, num))

    return getP(patterns)


def getLIMIT(prefix, type):
    if prefix == "YaHoo":
        if type == TYPE_DIGIT:
            LIMIT = LIMIT_DIGIT_YAHOO
        elif type == TYPE_CHAR:
            LIMIT = LIMIT_CHAR_YAHOO
        else:
            LIMIT = LIMIT_SPECIAL_YAHOO
    else:
        if type == TYPE_DIGIT:
            LIMIT = LIMIT_DIGIT_CSDN
        elif type == TYPE_CHAR:
            LIMIT = LIMIT_CHAR_CSDN
        else:
            LIMIT = LIMIT_SPECIAL_CSDN
    return LIMIT


def readAndBuild(prefix, type):
    fileName = BASE_DIR + prefix + "-%s.txt" % type
    inf = open(fileName, "r")
    lines = inf.readlines()
    inf.close()

    begin = False

    LIMIT = getLIMIT(prefix, type)

    dict = {}
    for i, line in enumerate(lines):
        line = line[:-1]
        if line == "-" * 40:
            begin = True
            continue

        if not begin:
            continue

        num = getNum(line)
        if num < LIMIT:
            print("get %d %s(used no less than %d times)" \
                  % (i + 1, type, LIMIT))
            for item in dict.items():
                dict[item[0]] = getP(item[1])
            return dict

        s = getStr(line)
        n = len(s)
        dict.setdefault(n, [])
        dict[n].append((s, num))

    for item in dict.items():
        dict[item[0]] = getP(item[1])
    return dict

def dfs(passwds, passwd, weight, pattern, digits, chars, specials):
    if len(pattern) == 0 or pattern[0] == '':
        passwds[passwd] = weight
        return

    type = pattern[0][0]
    num = int(pattern[0][1:])

    if type == "D":
        list = digits.setdefault(num, [])
    elif type == "A":
        list = chars.setdefault(num, [])
    else:
        list = specials.setdefault(num, [])

    for item in list:
        dfs(passwds, passwd + item[0], weight * item[1], pattern[1:], digits, chars, specials)

def solveTimes(pattern, digits, chars, specials):
    if pattern == [""]:
        return 1
    result = 1
    for part in pattern:
        type = part[0]
        num = int(part[1:])

        if type == "D":
            list = digits.setdefault(num, [])
        elif type == "A":
            list = chars.setdefault(num, [])
        else:
            list = specials.setdefault(num, [])
        result *= len(list)
    return result

def PCFG(prefix):
    patterns = readPatterns(prefix)

    digits = readAndBuild(prefix, TYPE_DIGIT)
    chars = readAndBuild(prefix, TYPE_CHAR)
    specials = readAndBuild(prefix, TYPE_SPECIAL)

    passwds = {}

    if prefix == "YaHoo":
        LIMIT = LIMIT_TIME_YAHOO
    else:
        LIMIT = LIMIT_TIME_CSDN

    n = len(patterns)
    for idx, patternAndNum in enumerate(patterns):
        pattern = patternAndNum[0].strip().split(" ")
        if solveTimes(pattern, digits, chars, specials) < LIMIT:
            dfs(passwds, "", patternAndNum[1], pattern, digits, chars, specials)
        else:
            print("ignore %s to save time" % "".join(pattern))

        if idx % ECHO == 0:
            print("processed %d/%d" % (idx, n))

    return passwds


def buildDictionary(prefix):
    passwds = getCommonPasswords(prefix)
    builtPasswds = PCFG(prefix)

    passwds.update(builtPasswds)
    return sorted(passwds.items(), key=lambda x:x[1], reverse=True)

if __name__ == '__main__':
    # parse the command
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hyc")
    except getopt.GetoptError:
        print("mainAnalyze.py [-y | -c]\n\t-y\tfor YaHoo\n\t-c\t for CSDN")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print("mainAnalyze.py [-y | -c]\n\t-y\tfor YaHoo\n\t-c\t for CSDN")
            sys.exit()
        elif opt == "-y":
            prefix = "YaHoo"
        elif opt == "-c":
            prefix = "CSDN"

    passwds = buildDictionary(prefix)
    outf = open(prefix + DICT_NAME, "w")
    for item in passwds:
        outf.write(item[0] + "\n")
    outf.close()
