from .chunker import Chunk
from .conv import morph as conv_morph
from .conv import posent as conv_posent
from .conv import pos as conv_pos
# import .statlog

class Rules():
    '''
    classdocs
    '''
    chunkID = 0
    currentChunk = 0
    prevChunk = 0
    currentSentence = 0
    # statlog = 0

    def __init__(self):
        '''
        Constructor
        '''

    def applyRulesInit(self, sentenceList):
        # self.statlog = goldcorpus.statlog.StatLog()
        for sentence in sentenceList:
            self.currentSentence = sentence
            self.applyRules(sentence)
            #print(sentence.id)
        # self.statlog.countChunks(sentenceList)
        # self.statlog.getRuleUsage()

    def applyRules(self, sentence):
        self.applyNP(sentence)
        self.currentChunk = 0
        self.prevChunk = 0
        self.applyVP(sentence)
        self.currentChunk = 0
        self.prevChunk = 0
        self.applyPP(sentence)
        self.currentChunk = 0
        self.prevChunk = 0
        self.applyADJP(sentence)
        self.currentChunk = 0
        self.prevChunk = 0
        self.applyADVP(sentence)
        self.currentChunk = 0
        self.prevChunk = 0
        self.applyMisc(sentence)
        self.currentChunk = 0
        self.prevChunk = 0
        self.removeEmptyChunks(sentence)
        self.sortChunks(sentence)
        self.splitGenetiv(sentence)


    def removeEmptyChunks(self, sentence):
        c = sentence.chunks
        for chunk in c:
            if(len(chunk.words) < 1):
                sentence.chunks.remove(chunk)
                print('Removing chunk ' + str(sentence.id))

    def sortChunks(self, sentence):
        for chunk in sentence.chunks:
            w = sorted(chunk.words, key=lambda w: w.id)
            chunk.words = w


    def splitGenetiv(self, sentence):
        for chunk in sentence.chunks:
            for n in range(0, len(chunk.words) - 1):
                word = chunk.words[n]
                morph = word.morph.replace("__", "|").strip().split('|')
                if(conv_morph('gen') in morph):
                    #print('Fant Genetiv')
                    start = True
                    genChunk = 0
                    for genWord in chunk.words[n+1:]:
                        if(start):
                            c = Chunk(self.chunkID, 'GNP')
                            self.chunkID = self.chunkID + 1
                            c.add_word(genWord)
                            c.setSentence(sentence)
                            sentence.add_chunk(c)
                            genWord.setChunk(c)
                            genChunk = c
                            start = False
                        else:
                            genChunk.add_word(genWord)
                            genWord.setChunk(genChunk)
                    chunk.words = chunk.words[0:n]
                    break


    def applyNP(self, sentence):
        type = 'NP'
        wordList = sentence.get_wordObjects()
        position = 1
        for word in wordList[1:]:
            #print(word.word + ' ' + word.type)

            #===================================================================
            # IF ord == subst
            #    THEN NP (b)
            #===================================================================

            if(word.type in conv_pos('subst')):
                #if(self.currentChunk == 0):
                #print('New chunk id ' + str(self.chunkID) + ' word: ' + word.word)
                chunk = Chunk(self.chunkID, type)
                self.chunkID = self.chunkID + 1
                chunk.add_word(word)
                chunk.setSentence(sentence)
                sentence.add_chunk(chunk)
                word.setChunk(chunk)
                self.currentChunk = chunk
                self.reverseApplyNP(wordList, position)
                # self.statlog.logRuleUsage('NP-subst-start')


            #===================================================================
            # IF ord == pron
            # THEN NP (b)
            #===================================================================

            elif(word.type in conv_pos('pron')):
                #if(self.currentChunk == 0):
                #print('New chunk id ' + str(self.chunkID) + ' word: ' + word.word)
                chunk = Chunk(self.chunkID, type)
                self.chunkID = self.chunkID + 1
                chunk.add_word(word)
                chunk.setSentence(sentence)
                sentence.add_chunk(chunk)
                word.setChunk(chunk)
                self.currentChunk = chunk
                # self.statlog.logRuleUsage('NP-pron-start')

            #===============================================================
            # IF ord == adj AND (peker- == subst AND  (Alle ord imellom == NP))
            # THEN NP (samme)
            #===============================================================

            elif(word.type in conv_pos('det')):
                if(word.head == (position - 1) and wordList[position-1].chunk.type == 'NP'):
                    self.currentChunk.add_word(word)
                    word.setChunk(self.currentChunk)

            else:
                self.currentChunk = 0
            position = position + 1

    def reverseApplyNP(self, wordList, position):
        for i in range(position-1,0,-1):
            word = wordList[i]
            cont = False
            #print('Reverse: ' + word.word)
            #===================================================================
            # IF ord == subst AND peker+- == (subst AND NP)
            #  THEN NP (samme)
            #===================================================================

            if(word.type in conv_pos('subst')):
                if(self.currentChunk != 0 and self.currentChunk.type == 'NP' and (self.searchForHeadInChunk(word) or self.searchForDepsInChunk(word))):
                    self.currentChunk.add_word(word)
                    if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
                        self.currentSentence.remove_chunk(word.getChunk())
                    word.setChunk(self.currentChunk)
                    cont = True

            #===================================================================
            # IF ord == konj AND peker+ == subst AND peker+ == NP
            #    THEN NP (samme)
            #===================================================================

            elif(word.type in conv_pos('konj')):
                if(self.currentChunk != 0 and self.currentChunk.type == 'NP' and self.searchForHeadInChunk(word)):
                    # Må sjekke om KONJP eller NP med å sjekke om hode til ord forran er i currentchunk
                    if(i > 1):
                        wordPrev = wordList[i - 1]
                        if(self.searchForHeadInChunk(wordPrev) or self.searchForDepsInChunk(wordPrev)):
                            self.currentChunk.add_word(word)
                            if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
                                self.currentSentence.remove_chunk(word.getChunk())
                            word.setChunk(self.currentChunk)
                            cont = True

            #===================================================================
            # IF ord == adv AND peker+ == adj AND peker+ == NP
            # THEN NP (samme)
            #===================================================================

            elif(word.type in conv_pos('adv')):
                if(self.currentChunk != 0 and self.currentChunk.type == 'NP' and self.searchForHeadInChunk(word)):
                    self.currentChunk.add_word(word)
                    if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
                        self.currentSentence.remove_chunk(word.getChunk())
                    word.setChunk(self.currentChunk)
                    cont = True

            #===============================================================
            # IF ord == adj AND (peker+ == subst AND (Alle ord imellom peker på subst + transistiv) AND (Alle ord imellom == NP))
            # THEN NP (samme)
            #===============================================================

            elif(word.type in conv_pos('adj')):
                if(self.currentChunk != 0 and self.currentChunk.type == 'NP' and (self.searchForHeadInChunk(word) or self.searchForDepsInChunk(word))):
                    self.currentChunk.add_word(word)
                    if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
                        self.currentSentence.remove_chunk(word.getChunk())
                    word.setChunk(self.currentChunk)
                    cont = True

            #====================================================================
            # IF ord == det AND peker- == subst AND (Alle ord imellom peker på subst + (transistiv) AND (Alle ord imellom == NP))
            # THEN NP (samme)
            #====================================================================

            elif(word.type in conv_pos('det')):
                if(self.currentChunk != 0 and self.currentChunk.type == 'NP' and (self.searchForHeadInChunk(word) or self.searchForDepsInChunk(word))):
                    self.currentChunk.add_word(word)
                    if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
                        self.currentSentence.remove_chunk(word.getChunk())
                    word.setChunk(self.currentChunk)
                    cont = True
            #===============================================================================
            # No possible chunk found,
            # return
            #===============================================================================
            if(not cont):
                return

    def applyVP(self, sentence):
        type = 'VP'
        wordList = sentence.get_wordObjects()
        position = 1
        for word in wordList[1:]:
            #print(word.word + ' ' + word.type)

            #===================================================================
            # IF ord == verb
            # THEN VP (b)
            #===================================================================

            if(word.type in conv_pos('verb')):
                #if(self.currentChunk == 0):
                #print('New chunk id ' + str(self.chunkID) + ' word: ' + word.word)
                chunk = Chunk(self.chunkID, type)
                self.chunkID = self.chunkID + 1
                chunk.add_word(word)
                chunk.setSentence(sentence)
                sentence.add_chunk(chunk)
                word.setChunk(chunk)
                self.currentChunk = chunk
                self.reverseApplyVP(wordList, position)
                # self.statlog.logRuleUsage('VP-verb-start')

            else:
                self.currentChunk = 0
            position = position + 1

    def reverseApplyVP(self, wordList, position):
        for i in range(position-1,0,-1):
            word = wordList[i]
            cont = False
            #print('Reverse: ' + word.word)

        #=======================================================================
        # IF ord == verb AND peker-+ == verb AND (Alle ord imellom peker på verb + (transistiv) AND (Alle ord imellom == VP))
        # THEN VP (samme)
        #=======================================================================
            if(word.getChunk().type == 'NP'):
                return

            if(word.type in conv_pos('verb')):
                if(self.currentChunk != 0 and self.currentChunk.type == 'VP' and (self.searchForHeadInChunk(word) or self.searchForDepsInChunk(word))):
                    self.currentChunk.add_word(word)
                    if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
                        self.currentSentence.remove_chunk(word.getChunk())
                    word.setChunk(self.currentChunk)
                    cont = True

        #=======================================================================
        # IF ord == adv AND peker+ == verb AND peker == ADV (Alle ord imellom peker på verb + (transistiv) AND (Alle ord imellom == VP))
        # THEN VP (samme)
        #=======================================================================

            if(word.type in conv_pos('adv')):
                if(self.currentChunk != 0 and self.currentChunk.type == 'VP' and self.searchForHeadInChunk(word) and word.posent.upper() == conv_posent('ADV')):
                    self.currentChunk.add_word(word)
                    if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
                        self.currentSentence.remove_chunk(word.getChunk())
                    word.setChunk(self.currentChunk)
                    cont = True

        #===========================================================================
        # IF ord == inf-merke AND peker+1 == verb # peker+1 i tilfelle det er noe imellom
        #    THEN VP (samme)
        #===========================================================================

            if(word.type in conv_pos('inf-merke')):
                if(self.currentChunk != 0 and self.currentChunk.type == 'VP' and (self.searchForHeadInChunk(word) or self.searchForDepsInChunk(word))):
                    self.currentChunk.add_word(word)
                    if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
                        self.currentSentence.remove_chunk(word.getChunk())
                    word.setChunk(self.currentChunk)
                    cont = True

            if(not cont):
                return

    def applyMisc(self,sentence):
        type = 'ERROR_IN_MISC'
        wordList = sentence.get_wordObjects()
        position = 1
        for n in range(1,len(wordList)):
            word = wordList[n]
            #print(word.word + ' ' + word.type)

            #===================================================================
            # IF ord == verb
            # THEN VP (b)
            #===================================================================

            if(word.type in conv_pos('sbu') and (word.posent == conv_posent('SBU') or word.posent == conv_posent('SBUREL') or word.posent == conv_posent('SUBJ') or word.posent == conv_posent('PUTFYLL') or word.posent == conv_posent('ADV'))):
                type = 'SBUP'
                chunk = Chunk(self.chunkID, type)
                self.chunkID = self.chunkID + 1
                chunk.add_word(word)
                chunk.setSentence(sentence)
                sentence.add_chunk(chunk)
                word.setChunk(chunk)
                # self.statlog.logRuleUsage('SBUP-sbu-start')

            elif(word.type in conv_pos('konj') and word.getChunk().type == '0'): #and word.posent == conv_posent('KONJ')
                type = 'CONJP'
                chunk = Chunk(self.chunkID, type)
                self.chunkID = self.chunkID + 1
                chunk.add_word(word)
                chunk.setSentence(sentence)
                sentence.add_chunk(chunk)
                word.setChunk(chunk)
                # self.statlog.logRuleUsage('CONJP-konj-start')
            #===================================================================
            # Denne fanger INTERJP, som i conll2000, veldig sjelden
            #===================================================================
            elif(word.type in conv_pos('interj') and word.chunk.id == -1):
                type = 'INTERJP'
                chunk = Chunk(self.chunkID, type)
                self.chunkID = self.chunkID + 1
                chunk.add_word(word)
                chunk.setSentence(sentence)
                sentence.add_chunk(chunk)
                word.setChunk(chunk)
                # self.statlog.logRuleUsage('INTERJP-interj-start')
            #===================================================================
            # Denne skal fange determinater forran adjektiver, der determinanten henger på et ord som er adjektivets hode
            # Se setning 1003, 'et gratis'
            #===================================================================
            elif(word.type in conv_pos('det') and word.chunk.id == -1 and word.head == wordList[n+1].head and wordList[n+1].chunk.id != -1):
                word.setChunk(wordList[n+1].chunk)
                wordList[n+1].chunk.add_word(word)
            #===================================================================
            # Denne skal fange det som henger på ord som er inne i anførselstegn, og er NP. Det blir en egen NP.
            # Se setning 31 'sin " onkel mulle"'
            #===================================================================
            elif(word.type in conv_pos('det') and word.chunk.id == -1 and wordList[word.head].chunk.type == 'NP'):# and word.head > word.id and word.head < (word.id + 5)):
                type = 'NP'
                chunk = Chunk(self.chunkID, type)
                self.chunkID = self.chunkID + 1
                chunk.add_word(word)
                chunk.setSentence(sentence)
                sentence.add_chunk(chunk)
                word.setChunk(chunk)
                # self.statlog.logRuleUsage('NP-det-start')
            #===================================================================
            # Denne skal fange det som er bak subjektet, men determinanten er hode (trolig feil i dep. analysen)
            # Se setning 10, KLOKKEN 20.25
            #===================================================================
            elif(word.type in conv_pos('det') and word.chunk.id == -1 and wordList[n-1].head == n and wordList[n-1].chunk.type == 'NP'):
                word.setChunk(wordList[n-1].chunk)
                wordList[n-1].chunk.add_word(word)
            #===================================================================
            # Denne skal fange dobble determinanter, der subjekt mangler, som gjør det til substitut subjekt.
            # Se setning 57, 'hans eget'
            #===================================================================
            elif(word.type in conv_pos('det') and word.chunk.id == -1 and wordList[n+1].id == word.head and wordList[n+1].chunk.id == -1 and wordList[n+1].type in conv_pos('det') and word.posent == conv_posent('DET')):
                type = 'NP'
                chunk = Chunk(self.chunkID, type)
                self.chunkID = self.chunkID + 1
                chunk.add_word(word)
                chunk.setSentence(sentence)
                sentence.add_chunk(chunk)
                word.setChunk(chunk)
                wordList[n+1].setChunk(chunk)
                chunk.add_word(wordList[n+1])
                # self.statlog.logRuleUsage('NP-det-start')
            #===================================================================
            # Denne skal fange dobble determinanter, der subjekt mangler, som gjør det til substitut subjekt. Her er ikke determinantene knyttet samme
            # Se setning 1108, 'en annen'. Merk at setningen ser ut til å mangle noen ord
            #===================================================================
            elif(word.type in conv_pos('det') and word.chunk.id == -1 and wordList[n+1].chunk.id == -1 and wordList[n+1].type in conv_pos('det') and word.posent == conv_posent('DET') and wordList[n+1].posent == conv_posent('DET')):
                type = 'NP'
                chunk = Chunk(self.chunkID, type)
                self.chunkID = self.chunkID + 1
                chunk.add_word(word)
                chunk.setSentence(sentence)
                sentence.add_chunk(chunk)
                word.setChunk(chunk)
                wordList[n+1].setChunk(chunk)
                chunk.add_word(wordList[n+1])
                # self.statlog.logRuleUsage('NP-det-start')
            #===================================================================
            # Denne skal fange dobble determinanter, der subjekt mangler, som gjør det til substitut subjekt. det er knyttet sammen.
            # Se setning 6091, '33 000'
            #===================================================================
            elif(word.type in conv_pos('det') and word.chunk.id == -1 and wordList[n+1].chunk.id == -1 and wordList[n+1].type in conv_pos('det') and wordList[n+1].id == word.head):
                type = 'NP'
                chunk = Chunk(self.chunkID, type)
                self.chunkID = self.chunkID + 1
                chunk.add_word(word)
                chunk.setSentence(sentence)
                sentence.add_chunk(chunk)
                word.setChunk(chunk)
                wordList[n+1].setChunk(chunk)
                chunk.add_word(wordList[n+1])
                # self.statlog.logRuleUsage('NP-det-start')
            #===================================================================
            # Denne skal fange det som hører til PP, der preposisjonen er depedent på det'en
            # Se setning 469, 'en av'
            #===================================================================
            elif(word.type in conv_pos('det') and word.chunk.id == -1 and wordList[n+1].head == word.id and wordList[n+1].chunk.type == 'PP' and wordList[n+1].posent == conv_posent('ATR')):
                word.setChunk(wordList[n+1].chunk)
                wordList[n+1].chunk.add_word(word)
            #===================================================================
            # Denne skal fange enslige det'ter der linken er SUBJ
            # Se setning 1984, 'Noe' og 3233, 'andre'
            #===================================================================
            #===================================================================
            # elif(word.type in conv_pos('det') and word.chunk.id == -1 and word.posent == conv_posent('SUBJ')):
            #    type = 'NP'
            #    chunk = Chunk(self.chunkID, type)
            #    self.chunkID = self.chunkID + 1
            #    chunk.add_word(word)
            #    chunk.setSentence(sentence)
            #    sentence.add_chunk(chunk)
            #    word.setChunk(chunk)
            #===================================================================
            #===================================================================
            # Denne skal fange enslige det'er der linken er SPRED eller OPRED eller DOBJ eller ADV eller KOORD-ELL eller SUBJ eller KOORD eller IK eller PUTFYLL eller DET
            # Se setning 2250, 1984, 3233, 2316, 2556, 2559, 994, 1030
            #===================================================================
            elif(word.type in conv_pos('det') and word.chunk.id == -1 and (word.posent == conv_posent('SPRED') or word.posent == conv_posent('OPRED') or word.posent == conv_posent('DOBJ') or word.posent == conv_posent('ADV') or word.posent == conv_posent('KOORD-ELL') or word.posent == conv_posent('SUBJ') or word.posent == conv_posent('KOORD') or word.posent == conv_posent('IK') or word.posent == conv_posent('PUTFYLL') or word.posent == conv_posent('DET'))):
                type = 'NP'
                chunk = Chunk(self.chunkID, type)
                self.chunkID = self.chunkID + 1
                chunk.add_word(word)
                chunk.setSentence(sentence)
                sentence.add_chunk(chunk)
                word.setChunk(chunk)
                # self.statlog.logRuleUsage('NP-det-start')
            #===================================================================
            # Denne skal fange enslige det'er der linken er KOORD
            # Se setning 2316
            #===================================================================
            #===================================================================
            # elif(word.type in conv_pos('det') and word.chunk.id == -1 and word.posent == conv_posent('KOORD')):
            #    type = 'NP'
            #    chunk = Chunk(self.chunkID, type)
            #    self.chunkID = self.chunkID + 1
            #    chunk.add_word(word)
            #    chunk.setSentence(sentence)
            #    sentence.add_chunk(chunk)
            #    word.setChunk(chunk)
            #===================================================================
            #===================================================================
            # Denne skal fange det der linken er IK eller PUTFYLL
            # Se setning 2556, '1' til 2559, '4'
            #===================================================================
            #===================================================================
            # elif(word.type in conv_pos('det') and word.chunk.id == -1 and (word.posent == conv_posent('IK') or word.posent == conv_posent('PUTFYLL'))):
            #    type = 'NP'
            #    chunk = Chunk(self.chunkID, type)
            #    self.chunkID = self.chunkID + 1
            #    chunk.add_word(word)
            #    chunk.setSentence(sentence)
            #    sentence.add_chunk(chunk)
            #    word.setChunk(chunk)
            #===================================================================
            #===================================================================
            # Denne skal fange type ufl, som kan være del av en PP, med PPen rett bakk
            # Se 2512, 'I går'
            #===================================================================
            elif(word.type in conv_pos('ufl') and word.chunk.id == -1 and wordList[word.head].chunk.type == 'PP' and word.head == (word.id - 1)):
                word.setChunk(wordList[word.head].chunk)
                wordList[word.head].chunk.add_word(word)
            #===================================================================
            # Denne skal fange ufl, som uflustendig del av en NP, der subjektet i NPen henger på ufl
            # Den tar samtidig å slår sammen en eventuelt foregående ADJP, hvis denne henger på ufl
            # Se setning 1114,  avis- og nettflora
            # Legger også til det som står rett før ufl, se setning 7708, 'andre'
            #===================================================================
            elif(word.type in conv_pos('ufl') and word.chunk.id == -1 and self.searchForDepsInChunkExt(word, wordList[n+1].chunk) and wordList[n+1].chunk.type == 'NP'):
                word.setChunk(wordList[n+1].chunk)
                wordList[n+1].chunk.add_word(word)
                currentChunk = wordList[n+1].chunk
                if(wordList[n-1].chunk.type == 'ADJP' and self.searchForDepsInChunkExt(word, wordList[n-1].chunk)):
                    sentence.remove_chunk(wordList[n-1].chunk)
                    for word in wordList[n-1].chunk.words:
                        word.setChunk(currentChunk)
                        currentChunk.add_word(word)
                if(wordList[n-1].head == word.id and wordList[n-1].type in conv_pos('det')):
                    if(wordList[n-1].chunk.id != -1):
                        wordList[n-1].chunk.remove_word(wordList[n-1])
                    wordList[n-1].setChunk(currentChunk)
                    currentChunk.add_word(wordList[n-1])
            #===================================================================
            # Denne skal fange ufl der to ufl er skilt med en konj, slik at de kan slåes sammen til en NP
            # Se setning 1415 'brask og bram'
            #===================================================================
            elif(word.type in conv_pos('ufl') and word.chunk.id == -1 and wordList[word.head].type in conv_pos('ufl') and wordList[n-1].type in conv_pos('konj') and wordList[n-1].head == word.id):
                type = 'NP'
                chunk = Chunk(self.chunkID, type)
                self.chunkID = self.chunkID + 1
                chunk.add_word(word)
                chunk.setSentence(sentence)
                sentence.add_chunk(chunk)
                word.setChunk(chunk)
                wordList[n-1].chunk.remove_word(wordList[n-1])
                wordList[n-1].setChunk(chunk)
                chunk.add_word(wordList[n-1])
                wordList[word.head].chunk.remove_word(wordList[word.head])
                wordList[word.head].setChunk(chunk)
                chunk.add_word(wordList[word.head])
                # self.statlog.logRuleUsage('NP-ufl-start')
            #===================================================================
            # Denne skal fange ufl der ufl henger på subjeket
            # Se setning 2344
            #===================================================================
            elif(word.type in conv_pos('ufl') and word.chunk.id == -1 and wordList[word.head].type in conv_pos('subst')):
                word.setChunk(wordList[word.head].chunk)
                wordList[word.head].chunk.add_word(word)
            #===================================================================
            # Denne skal fange ufl der den skal være del av en ADJP som er depedent på ufl, og ADJP er rett før ufl
            # Se setning 3891, 'fjor'
            #===================================================================
            elif(word.type in conv_pos('ufl') and word.chunk.id == -1 and wordList[n-1].head == word.id and wordList[n-1].chunk.type == 'ADJP'):
                word.setChunk(wordList[n-1].chunk)
                wordList[n-1].chunk.add_word(word)
            #===================================================================
            # Denne skal fange noen forkortelser, og sette NP.
            # Se 463 'F Eks'
            #===================================================================
            elif(word.type in conv_pos('fork') and word.chunk.id == -1 and wordList[n+1].head == word.id and wordList[n+1].type in conv_pos('fork')):
                type = 'NP'
                chunk = Chunk(self.chunkID, type)
                self.chunkID = self.chunkID + 1
                chunk.add_word(word)
                chunk.setSentence(sentence)
                sentence.add_chunk(chunk)
                word.setChunk(chunk)
                wordList[n+1].setChunk(chunk)
                chunk.add_word(wordList[n+1])
                # self.statlog.logRuleUsage('NP-fork-start')
            #===================================================================
            # Denne skal fange inf-merke som henger på en pp
            # Se setning 2890, 'å'
            #===================================================================
            elif(word.type in conv_pos('inf-merke') and word.chunk.id == -1):
                dep_check_true = False
                for dw in word.deps:
                    if(wordList[dw].head == word.id and wordList[dw].chunk.type == 'VP'):
                        dep_check_true = True
                if(dep_check_true):
                    type = 'VP'
                    chunk = Chunk(self.chunkID, type)
                    self.chunkID = self.chunkID + 1
                    chunk.add_word(word)
                    chunk.setSentence(sentence)
                    sentence.add_chunk(chunk)
                    word.setChunk(chunk)
                    # self.statlog.logRuleUsage('VP-inf-merke-start')
            #===================================================================
            # Skal fange type 'dem' hvis koblet til ADJP
            # Se setning 5528 det motsatte ('dem'???)
            #===================================================================
            #===================================================================
            # elif(word.type in conv_pos('dem') and word.chunk.id == -1 and word.posent == conv_posent('DET') and word.head == wordList[n+1].id and wordList[n+1].type in conv_pos('adj') and wordList[n+1].chunk.type == 'ADJP'):
            #    wordList[word.head].chunk.add_word(word)
            #    word.setChunk(wordList[word.head].chunk)
            #===================================================================
            #===================================================================
            # Denne skal fange flerleddedde egennavn, merket med første ord subst,prop og alle depedenter på denne har FLAT
            # Se setning 7708, 'Den Norske Kirke'
            #===================================================================
            elif(word.type in conv_pos('subst')):
                morph = word.morph.replace("__", "|").strip().split('|')
                if(conv_morph('prop') in morph):
                    wordsToInclude = []
                    for n in range(word.id + 1,len(wordList)):
                        wordNext = wordList[n]
                        stop = False
                        if(not stop and wordNext.posent == conv_posent('FLAT') and wordNext.head == word.id):
                            wordsToInclude.append(wordNext)
                        else:
                            stop = True
                    if(len(wordsToInclude) > 0):
                        type = 'NP'
                        chunk = Chunk(self.chunkID, type)
                        self.chunkID = self.chunkID + 1
                        chunk.add_word(word)
                        chunk.setSentence(sentence)
                        sentence.add_chunk(chunk)
                        word.chunk.remove_word(word)
                        word.setChunk(chunk)
                        for w in wordsToInclude:
                            if(w.chunk.id != -1):
                                w.chunk.remove_word(w)
                            w.setChunk(chunk)
                            chunk.add_word(w)
            else:
                self.currentChunk = 0
            position = position + 1

            # Utestådende problemer:
            # 'Intet annet' i 1011
            # '15000 i' i 1018

    def applyPP(self, sentence):
        type = 'PP'
        wordList = sentence.get_wordObjects()
        position = 1
        for word in wordList[1:]:
            #print(word.word + ' ' + word.type)

            #===================================================================
            # IF ord == verb
            # THEN VP (b)
            #===================================================================
            if(word.getChunk().type == 'NP' or word.getChunk().type == 'VP'):
                pass
            elif(word.type in conv_pos('prep')):
                chunk = Chunk(self.chunkID, type)
                self.chunkID = self.chunkID + 1
                chunk.add_word(word)
                chunk.setSentence(sentence)
                sentence.add_chunk(chunk)
                word.setChunk(chunk)
                self.currentChunk = chunk
                self.reverseApplyPP(wordList, position)
            # Denne skal fange tilfeller der determinanten hører til PP, og står BAK pp
            elif(word.type in conv_pos('det') and self.currentChunk != 0 and self.currentChunk.type == 'PP' and self.searchForHeadInChunkNoTrans(word)):
                self.currentChunk.add_word(word)
                if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
                    self.currentSentence.remove_chunk(word.getChunk())
                word.setChunk(self.currentChunk)
            else:
                self.currentChunk = 0
            position = position + 1

    def reverseApplyPP(self, wordList, position):
        for i in range(position-1,0,-1):
            word = wordList[i]
            cont = False
            #print('Reverse: ' + word.word)

        #=======================================================================
        # IF ord == verb AND peker-+ == verb AND (Alle ord imellom peker på verb + (transistiv) AND (Alle ord imellom == VP))
        # THEN VP (samme)
        #=======================================================================
            if(word.getChunk().type == 'NP' or word.getChunk().type == 'VP'):
                return

            if(word.type in conv_pos('prep')):
                if(self.currentChunk != 0 and self.currentChunk.type == 'PP' and (self.searchForHeadInChunk(word) or self.searchForDepsInChunk(word))):
                    self.currentChunk.add_word(word)
                    if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
                        self.currentSentence.remove_chunk(word.getChunk())
                    word.setChunk(self.currentChunk)
                    cont = True

            if(not cont):
                return

    def applyADJP(self, sentence):
        type = 'ADJP'
        wordList = sentence.get_wordObjects()
        position = 1
        for word in wordList[1:]:
            #print(word.word + ' ' + word.type)

            #===================================================================
            # IF ord == verb
            # THEN VP (b)
            #===================================================================
            if(word.getChunk().type == 'NP' or word.getChunk().type == 'VP' or word.getChunk().type == 'PP'):
                pass

            elif(word.type in conv_pos('adj')):
                chunk = Chunk(self.chunkID, type)
                self.chunkID = self.chunkID + 1
                chunk.add_word(word)
                chunk.setSentence(sentence)
                sentence.add_chunk(chunk)
                word.setChunk(chunk)
                self.currentChunk = chunk
                self.reverseApplyADJP(wordList, position)

            else:
                self.currentChunk = 0
            position = position + 1

    def reverseApplyADJP(self, wordList, position):
        for i in range(position-1,0,-1):
            word = wordList[i]
            cont = False
            #print('Reverse: ' + word.word)

        #=======================================================================
        # IF ord == verb AND peker-+ == verb AND (Alle ord imellom peker på verb + (transistiv) AND (Alle ord imellom == VP))
        # THEN VP (samme)
        #=======================================================================
            if(word.getChunk().type == 'NP' or word.getChunk().type == 'VP' or word.getChunk().type == 'PP'):
                return

            if(word.type in conv_pos('adj')):
                if(self.currentChunk != 0 and self.currentChunk.type == 'ADJP' and (self.searchForHeadInChunk(word) or self.searchForDepsInChunk(word))):
                    self.currentChunk.add_word(word)
                    if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
                        self.currentSentence.remove_chunk(word.getChunk())
                    word.setChunk(self.currentChunk)
                    cont = True

            if(word.type in conv_pos('adv')):
                if(self.currentChunk != 0 and self.currentChunk.type == 'ADJP' and (self.searchForHeadInChunk(word) or self.searchForDepsInChunk(word))):
                    self.currentChunk.add_word(word)
                    if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
                        self.currentSentence.remove_chunk(word.getChunk())
                    word.setChunk(self.currentChunk)
                    cont = True

            if(word.type in conv_pos('det')):
                if(self.currentChunk != 0 and self.currentChunk.type == 'ADJP' and (self.searchForHeadInChunk(word) or self.searchForDepsInChunk(word))):
                    self.currentChunk.add_word(word)
                    if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
                        self.currentSentence.remove_chunk(word.getChunk())
                    word.setChunk(self.currentChunk)
                    cont = True

            if(not cont):
                return

    def applyADVP(self, sentence):
        type = 'ADVP'
        wordList = sentence.get_wordObjects()
        position = 1
        for word in wordList[1:]:
            #print(word.word + ' ' + word.type)

            #===================================================================
            # IF ord == verb
            # THEN VP (b)
            #===================================================================
            if(word.getChunk().type == 'NP' or word.getChunk().type == 'VP' or word.getChunk().type == 'PP' or word.getChunk().type == 'ADJP'):
                pass
            elif(word.type in conv_pos('adv')):
                chunk = Chunk(self.chunkID, type)
                self.chunkID = self.chunkID + 1
                chunk.add_word(word)
                chunk.setSentence(sentence)
                sentence.add_chunk(chunk)
                word.setChunk(chunk)
                self.currentChunk = chunk
                self.reverseApplyADVP(wordList, position)

            else:
                self.currentChunk = 0
            position = position + 1

    def reverseApplyADVP(self, wordList, position):
        for i in range(position-1,0,-1):
            word = wordList[i]
            cont = False
            #print('Reverse: ' + word.word)

        #=======================================================================
        # IF ord == verb AND peker-+ == verb AND (Alle ord imellom peker på verb + (transistiv) AND (Alle ord imellom == VP))
        # THEN VP (samme)
        #=======================================================================
            if(word.getChunk().type == 'NP' or word.getChunk().type == 'VP' or word.getChunk().type == 'PP' or word.getChunk().type == 'ADJP'):
                return

            if(word.type in conv_pos('adv')):
                if(self.currentChunk != 0 and self.currentChunk.type == 'ADVP' and (self.searchForHeadInChunk(word) or self.searchForDepsInChunk(word))):
                    self.currentChunk.add_word(word)
                    if(word.getChunk().id != -1 and word.getChunk() != self.currentChunk and word.getChunk() in self.currentSentence.chunks):
                        self.currentSentence.remove_chunk(word.getChunk())
                    word.setChunk(self.currentChunk)
                    cont = True

            if(not cont):
                return

    def searchForHeadInChunk(self, word):
        for wordInChunk in self.currentChunk.words:
            if(word.head == wordInChunk.id): # Kan også ha skjekk for om ord er subst eller adj eller pron
                return True
            head_of_word = self.currentSentence.get_word_at_position(word.head)
            if(head_of_word.head == wordInChunk.id):
                #print(head_of_word.word + ' ' + str(self.currentSentence.id))
                return True
        return False
            # Legg inn transtivitet

    def searchForHeadInChunkNoTrans(self, word):
        for wordInChunk in self.currentChunk.words:
            if(word.head == wordInChunk.id): # Kan også ha skjekk for om ord er subst eller adj eller pron
                return True
        return False

    def searchForDepsInChunk(self, word):
        for wordInChunk in self.currentChunk.words:
            if(wordInChunk.id in word.deps):
                return True
        return False

    def searchForDepsInChunkExt(self, word, chunk):
        for wordInChunk in chunk.words:
            if(wordInChunk.id in word.deps):
                return True
        return False
