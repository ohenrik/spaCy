from __future__ import unicode_literals

from ...symbols import NOUN, PROPN, PRON, AUX, VERB


def noun_chunks(obj):
    pass
    self.applyNP(sentence)
    # self.currentChunk = 0
    # self.prevChunk = 0
    # self.applyVP(sentence)
    # self.currentChunk = 0
    # self.prevChunk = 0
    # self.applyPP(sentence)
    # self.currentChunk = 0
    # self.prevChunk = 0
    # self.applyADJP(sentence)
    # self.currentChunk = 0
    # self.prevChunk = 0
    # self.applyADVP(sentence)
    # self.currentChunk = 0
    # self.prevChunk = 0
    # self.applyMisc(sentence)
    # self.currentChunk = 0
    # self.prevChunk = 0
    # self.removeEmptyChunks(sentence)
    # self.sortChunks(sentence)
    # self.splitGenetiv(sentence)

def applyNP(doc):
    type = 'NP'
    position = 1
    for word in doc:
        print(word, word.dep_, word.pos_, word.i, word.right_edge, word.left_edge)
        #print(word.word + ' ' + word.type)

        #===================================================================
        # IF ord == subst
        #    THEN NP (b)
        #===================================================================

        if(word.pos in [NOUN, PROPN]):
        #     #if(self.currentChunk == 0):
        #     #print('New chunk id ' + str(self.chunkID) + ' word: ' + word.word)
        #     chunk = goldcorpus.chunk.Chunk(self.chunkID, type)
        #     self.chunkID = self.chunkID + 1
        #     chunk.add_word(word)
        #     chunk.setSentence(sentence)
        #     sentence.add_chunk(chunk)
        #     word.setChunk(chunk)
        #     self.currentChunk = chunk
            reverseApplyNP(doc, word.i)
        #     self.statlog.logRuleUsage('NP-subst-start')
        # #
        #
        # #===================================================================
        # # IF ord == pron
        # # THEN NP (b)
        # #===================================================================
        #
        # elif(word.type == 'pron'):
        #     #if(self.currentChunk == 0):
        #     #print('New chunk id ' + str(self.chunkID) + ' word: ' + word.word)
        #     chunk = goldcorpus.chunk.Chunk(self.chunkID, type)
        #     self.chunkID = self.chunkID + 1
        #     chunk.add_word(word)
        #     chunk.setSentence(sentence)
        #     sentence.add_chunk(chunk)
        #     word.setChunk(chunk)
        #     self.currentChunk = chunk
        #     self.statlog.logRuleUsage('NP-pron-start')
        #
        # #===============================================================
        # # IF ord == adj AND (peker- == subst AND  (Alle ord imellom == NP))
        # # THEN NP (samme)
        # #===============================================================
        #
        # elif(word.type == 'det'):
        #     if(word.head == (position - 1) and wordList[position-1].chunk.type == 'NP'):
        #         self.currentChunk.add_word(word)
        #         word.setChunk(self.currentChunk)
        #
        # else:
        #     self.currentChunk = 0
        # position = position + 1

def reverseApplyNP(doc, position):
    for i in range(position-1,0,-1):
        word = wordList[i]
        cont = False
        #print('Reverse: ' + word.word)
        #===================================================================
        # IF ord == subst AND peker+- == (subst AND NP)
        #  THEN NP (samme)
        #===================================================================

        if(word.pos in [NOUN, PROPN]):
            if(self.currentChunk != 0 and self.currentChunk.type == 'NP' and (self.searchForHeadInChunk(word) or self.searchForDepsInChunk(word))):
                self.currentChunk.add_word(word)
                if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
                    self.currentSentence.remove_chunk(word.getChunk())
                word.setChunk(self.currentChunk)
                # cont = True

        # #===================================================================
        # # IF ord == konj AND peker+ == subst AND peker+ == NP
        # #    THEN NP (samme)
        # #===================================================================
        #
        # elif(word.type == 'konj'):
        #     if(self.currentChunk != 0 and self.currentChunk.type == 'NP' and self.searchForHeadInChunk(word)):
        #         # Må sjekke om KONJP eller NP med å sjekke om hode til ord forran er i currentchunk
        #         if(i > 1):
        #             wordPrev = wordList[i - 1]
        #             if(self.searchForHeadInChunk(wordPrev) or self.searchForDepsInChunk(wordPrev)):
        #                 self.currentChunk.add_word(word)
        #                 if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
        #                     self.currentSentence.remove_chunk(word.getChunk())
        #                 word.setChunk(self.currentChunk)
        #                 cont = True
        #
        # #===================================================================
        # # IF ord == adv AND peker+ == adj AND peker+ == NP
        # # THEN NP (samme)
        # #===================================================================
        #
        # elif(word.type == 'adv'):
        #     if(self.currentChunk != 0 and self.currentChunk.type == 'NP' and self.searchForHeadInChunk(word)):
        #         self.currentChunk.add_word(word)
        #         if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
        #             self.currentSentence.remove_chunk(word.getChunk())
        #         word.setChunk(self.currentChunk)
        #         cont = True
        #
        # #===============================================================
        # # IF ord == adj AND (peker+ == subst AND (Alle ord imellom peker på subst + transistiv) AND (Alle ord imellom == NP))
        # # THEN NP (samme)
        # #===============================================================
        #
        # elif(word.type == 'adj'):
        #     if(self.currentChunk != 0 and self.currentChunk.type == 'NP' and (self.searchForHeadInChunk(word) or self.searchForDepsInChunk(word))):
        #         self.currentChunk.add_word(word)
        #         if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
        #             self.currentSentence.remove_chunk(word.getChunk())
        #         word.setChunk(self.currentChunk)
        #         cont = True
        #
        # #====================================================================
        # # IF ord == det AND peker- == subst AND (Alle ord imellom peker på subst + (transistiv) AND (Alle ord imellom == NP))
        # # THEN NP (samme)
        # #====================================================================
        #
        # elif(word.type == 'det'):
        #     if(self.currentChunk != 0 and self.currentChunk.type == 'NP' and (self.searchForHeadInChunk(word) or self.searchForDepsInChunk(word))):
        #         self.currentChunk.add_word(word)
        #         if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
        #             self.currentSentence.remove_chunk(word.getChunk())
        #         word.setChunk(self.currentChunk)
        #         cont = True
        # #===============================================================================
        # # No possible chunk found,
        # # return
        # #===============================================================================
        # if(not cont):
        #     return


# def noun_chunks(obj):
#     """
#     Detect base noun phrases from a dependency parse. Works on both Doc and Span.
#     """
#     labels = ['nsubj', 'dobj', 'nsubjpass', 'pcomp', 'pobj', 'dative', 'appos',
#               'attr', 'ROOT']
#     doc = obj.doc # Ensure works on both Doc and Span.
#     np_deps = [doc.vocab.strings.add(label) for label in labels]
#     conj = doc.vocab.strings.add('conj')
#     np_label = doc.vocab.strings.add('NP')
#     seen = set()
#     for i, word in enumerate(obj):
#         if word.pos not in (NOUN, PROPN, PRON):
#             continue
#         # Prevent nested chunks from being produced
#         if word.i in seen:
#             continue
#         if word.dep in np_deps:
#             if any(w.i in seen for w in word.subtree):
#                 continue
#             seen.update(j for j in range(word.left_edge.i, word.i+1))
#             yield word.left_edge.i, word.i+1, np_label
#         elif word.dep == conj:
#             head = word.head
#             while head.dep == conj and head.head.i < head.i:
#                 head = head.head
#             # If the head is an NP, and we're coordinated to it, we're an NP
#             if head.dep in np_deps:
#                 if any(w.i in seen for w in word.subtree):
#                     continue
#                 seen.update(j for j in range(word.left_edge.i, word.i+1))
#                 yield word.left_edge.i, word.i+1, np_label


SYNTAX_ITERATORS = {
    'noun_chunks': noun_chunks
}
