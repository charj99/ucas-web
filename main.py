import sys, getopt
from YaHoo import YaHoo
from CSDN import CSDN
from nltk.corpus import names, words


if __name__ == '__main__':
    # parse the command
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hyc")
    except getopt.GetoptError:
        print("main.py [-y | -c]\n\t-y\tfor YaHoo\n\t-c\t for CSDN")
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print("main.py [-y | -c]\n\t-y\tfor YaHoo\n\t-c\t for CSDN")
            sys.exit()
        elif opt == "-y":
            solver = YaHoo()
        elif opt == "-c":
            solver = CSDN()

    WORDS = words.words("en")
    NAMES = names.words("male.txt") + names.words("female.txt")
    WORDS = [x.lower() for x in WORDS]
    NAMES = [x.lower() for x in NAMES]

    # TODO: 用户名、邮箱和 passwd 关系分析
    # solver.analyzeComponent()
    # solver.analyzeKeyboard()
    solver.analyzePinyin(WORDS, NAMES)

