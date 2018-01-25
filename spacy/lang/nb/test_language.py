import spacy
from spacy.lang.nb.noun_chunker.rules import Rules
from spacy.lang.nb.noun_chunker.sentence import Sentence
from spacy import displacy
# model = spacy.load('/home/ohenrik/ads-projectdata/upfeed_analyser/data/models/small2/model7')
model = spacy.load('/Users/ohenrik/Sites/upfeed_analyser/data/models/small6/model7')

doc1 = model('Det året jeg fylte 18, døde bestefaren min')
doc1 = model('I går døde bestefaren min')

# doc2 = model('Utvalget har fulgt opp dette, og også beskrevet de viktigste konsekvensene som de ulike alternativene innebærer for staten, Den norske kirke og andre tros- og livssynssamfunn.')
doc2 = model('Utvalget har fulgt opp dette, og også beskrevet de viktigste konsekvensene som de ulike alternativene innebærer for staten, Den norske kirke og andre livssynssamfunn.')


def printTokens(doc):
    for token in doc:
            print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)

# printTokens(doc)

sent1 = Sentence(0, doc1)
sent2 = Sentence(0, doc2)
res1 = Rules().applyRulesInit([sent1])
res2 = Rules().applyRulesInit([sent2])
# res = Rules().applyRules(sent)
def printStr(sent):
    for chunk in sent.chunks:
        words = [word.word + " " + word.type for word in chunk.words]
        heads = [word.head for word in chunk.words]
        print(words, chunk.id, chunk.type, heads, sent.get_word_list()[heads[0]])

printStr(sent1)
print()
printStr(sent2)
# import pdb; pdb.set_trace()
