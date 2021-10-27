from base import Base
from base import INPUTFILE_CSDN, SEPERATOR_CSDN

class CSDN(Base):
    def __init__(self):
        super().__init__("CSDN", INPUTFILE_CSDN)

    def getPasswd(self, line):
        return line[:-2].split(SEPERATOR_CSDN)[1]

    def analyzeComponent(self):
        super().analyzeComponent()

    def analyzePinyin(self):
        super().analyzePinyin()