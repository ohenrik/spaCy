import spacy
from spacy.lang.nb.noun_chunker.rules import Rules
from spacy.lang.nb.noun_chunker.sentence import Sentence
from spacy import displacy
# model = spacy.load('/home/ohenrik/ads-projectdata/upfeed_analyser/data/models/small2/model7')
model = spacy.load('/Users/ohenrik/Sites/upfeed_analyser/data/models/small7/model7')


sentances = [
    # model('Den unge kvinnen som har varslet om det hun opplevde som uønskede seksuelle tilnærmelser fra Trond Giskes side da hun selv var ung AUFer, er også fornøyd.'),
    # model('Varselet til partiet ga hun med fullt navn. Hun ønsker ikke å stå frem med navn i Aftenposten, men Aftenposten kjenner hennes identitet.'),
    # model('Jeg våkner ikke opp hjemme.'),
    # model('Det tar noen brøkdeler av et sekund før jeg skjønner dette.'),
    # model('Før jeg skjønner at jeg ikke er hjemme på kjøkkenet mitt, med kaffekoppen min og den deilige utsikten mot skogen.'),
    # model('Jeg kniper øynene igjen og tenker på hjemme et par sekunder til.'),
    # model('Så åpner jeg dem. Det er mørkt.'),
    # model('Jeg kan høre gongen jome fra flere steder, da verten beveger seg rundt i bygget, mellom etasjene, for å vekke alle sammen.'),
    model('Du prøver å video blogge for å få opp leser tallet'),
    model('Du prøver å videoblogge for å få opp lesertallet'),
    model('en spørsmålsrunde burde komme fordi du får mange spm å bestemmer deg for å svare på de på engang!'),
    model('en spørsmålsrunde burde komme fordi du får mange spørsmål og bestemmer deg for å svare på dem på engang!'),
    model('Så i går var det pepperkake baking, julemusikk og gløgg.'),
    model('Så i går var det pepperkakebaking, julemusikk og gløgg.'),
    model('Kjempe stemning og nellik appelsinene sprer god duft hjemme.'),
    model('Kjempestemning og nellik appelsinene sprer god duft hjemme.'),
    model('Jeg hadde med meg et Gods tog.'),
    model('Jeg hadde med meg et Godstog.'),
    model('Jeg bor i et fyr tårn'),
    model('Jeg bor i et fyrtårn'),
    # model('Det året jeg fylte 18, døde bestefaren min'),
    # model('I går døde bestefaren min'),
    # model('Jeg vil ha en blå ballong.'),
    # model('En blå ballong, vil jeg ha.'),
    # model('Utvalget har fulgt opp dette, og også beskrevet de viktigste konsekvensene som de ulike alternativene innebærer for staten, Den norske kirke og andre tros- og livssynssamfunn.'),
    # model('Utvalget har fulgt opp dette, og også beskrevet de viktigste konsekvensene som de ulike alternativene innebærer for staten, Den norske kirke og andre livssynssamfunn.'),
]



def printTokens(doc):
    for token in doc:
            print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)

# printTokens(doc)
sent_loaded = []
for sent in sentances:
    parsed = Sentence(0, sent)
    Rules().applyRulesInit([parsed])
    sent_loaded.append(parsed)


# res = Rules().applyRules(sent)
def printStr(sent):
    for chunk in sent.chunks:
        #+ " " + word.type
        words = [word.word  for word in chunk.words]
        heads = [word.head for word in chunk.words]
        root = sent.get_wordObjects()[heads[0]]
        print(str(words) + ";" + chunk.type + (";(" + root.word + " " + root.posent + ")"))

for sent in sent_loaded:
    printStr(sent)
    printTokens(sent.doc)
    print()

displacy.serve([sent.doc for sent in sent_loaded],style='dep')
