from base import Base
from base import INPUTFILE_YAHOO, SEPERATOR_YAHOO

class YaHoo(Base):
    def __init__(self):
        super().__init__("YaHoo", INPUTFILE_YAHOO)

    def getPasswd(self, line):
        return line[:-2].split(SEPERATOR_YAHOO)[-1]

    def analyzeComponent(self):
        super().analyzeComponent()

    def analyzePinyin(self):
        super().analyzePinyin()