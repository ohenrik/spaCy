from .word import Word

class Sentence():
    doc = None
    words = []
    chunks = []
    id = -1



    def __init__(self, id, sentence=None):
        '''
        Constructor
        '''
        self.id = id
        self.doc = sentence
        # self.words = doc
        self.words = []
        self.words.append(Word(None))
        for word in sentence:
            self.words.append(Word(word))
        self.calc_dependencys()
        self.chunks = []

    def calc_dependencys(self):
        #for word in self.words[1:]:
        for word in self.words:
            self.words[word.head].deps.append(int(word.id))

    def get_word_list(self):
        return [word.word for word in self.words]

    def get_wordObjects(self):
        return self.words

    def get_id_list(self):
        return [word.id for word in self.words]

    def get_word_at_position(self, pos):
        return self.words[pos]

    def get_deps_list(self):
        r = []
        for word in self.words:
            r.append(word.deps)
        return r

    def get_head_list(self):
        r = []
        for word in self.words:
            r.append(word.head)
        return r

    def add_chunk(self, chunk):
        self.chunks.append(chunk)

    def remove_chunk(self, chunk):
        self.chunks.remove(chunk)
