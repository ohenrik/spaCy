"""Chunk"""

class Chunk():
    type_ = ''
    words = []
    id_ = 0
    sentence = 0

    def __init__(self, id_, type_):
        self.type = type_
        self.id = id_
        self.words = []

    def add_word(self, word):
        self.words.append(word)

    def remove_word(self, word):
        self.words.remove(word)

    def setSentence(self, sentence):
        self.sentence = sentence
