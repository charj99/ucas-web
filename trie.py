class PyTrieNode(object):
    def __init__(self, key=b"", seq=b""):
        self.key = key
        self.end = len(seq) == 0
        self.children = {}
        if len(seq) > 0:
            self.children[seq[0:1]] = PyTrieNode(seq[0:1], seq[1:])

    def add(self, seq):
        if len(seq) == 0:
            self.end = True
        else:
            key = seq[0:1]
            value = seq[1:]
            if key in self.children:
                self.children[key].add(value)
            else:
                self.children[key] = PyTrieNode(key, value)

    def find(self, sent):
        if len(sent) == 0:
            return b"", self.end
        key = sent[0:1]
        if key in self.children:
            buf, succ = self.children[key].find(sent[1:])
            return key + buf, succ
        else:
            return b"", self.end


class PyTrie(object):
    def __init__(self):
        self.root = PyTrieNode()
        self.root.end = False

    def setup(self):
        inf = open("pinyin.txt", "rb")
        lines = inf.readlines()
        for line in lines:
            self.add(line[:-2])
        inf.close()

    def add(self, seq):
        self.root.add(seq)

    def scan(self, sent):
        words = []
        flag = True
        count = 0
        while len(sent) > 0:
            buf, succ = self.root.find(sent)
            if succ:
                words.append(buf)
                sent = sent[len(buf):]
                count += 1
            else:
                flag = False
                words.append(b'invalid:' + sent[0:1])
                sent = sent[1:]
        return words, flag

