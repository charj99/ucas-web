INPUTFILE_YAHOO = "plaintxt_yahoo.txt"
INPUTFILE_CSDN = "www.csdn.net.sql"

def getPattern(passwd, nChrDict):
    pattern = ""
    lstType = "S" # magic begin
    curType = ""
    for letter in passwd:
        if str.isdigit(letter):
            curType = "D"
        elif str.isalpha(letter):
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
