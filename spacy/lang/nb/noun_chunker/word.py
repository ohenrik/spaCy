from .chunker import Chunk

class Word():
    id = 0
    word = 'NA'
    lowerword = 'na'
    type = 'no_type'
    type_other = 'no_type'
    morph = 'gibber'
    head = -1
    posent = 'NOTPART'
    other1 = 'N_'
    other2 = 'N_'
    deps = []
    chunk = 0

    def __init__(self, word=None):
        '''
        Constructor
        '''
        if word:
            self.id = word.i + 1
            self.word = str(word)
            self.lowerword = str(word).lower()
            self.type = word.pos_
            self.morph = word.tag_
            self.head = word.head.i + 1
            self.posent = word.dep_
            self.deps = []
            self.chunk = Chunk(-1, '0')

    def setChunk(self, chunk):
        self.chunk = chunk

    def getChunk(self):
        return self.chunk
