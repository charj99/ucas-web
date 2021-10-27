import sys, getopt
from YaHoo import YaHoo
from CSDN import CSDN


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
            solver = YaHoo()
        elif opt == "-c":
            solver = CSDN()


    '''
        1. calculate different passwords,   and save to "YaHoo/CSDN-passwords.txt"
        2. calculate password patterns,     and save to "YaHoo/CSDN-patterns.txt"
        3. calculate digital sequences,     and save to "YaHoo/CSDN-digits.txt"
        4. calculate character sequences,   and save to "YaHoo/CSDN-characters.txt"
        5. calculate other sequences,       and save to "YaHoo/CSDD-specials.txt"
        6. caluclate diffent email types,   and save to "YaHoo/CSDN-emails.txt"
    '''
    # solver.analyzeComponent()

    '''
        1. calculate different pinyins,     and save to "YaHoo/CSDN-pinyins.txt"
        2. calculate different words,       and save to "YaHoo/CSDN-words.txt"
    '''
    # solver.analyzePinyin()

    '''
        1. calculate how many password are the same as id or email, 
            and save to "YaHoo/relations.txt"
    '''
    solver.analyzeRelation()

