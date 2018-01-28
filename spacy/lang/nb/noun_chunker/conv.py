"""Converter module from OBT to UD

Using this conversion:
http://www.lrec-conf.org/proceedings/lrec2016/pdf/462_Paper.pdf

"""

pos_dict = {
    'adj': ['ADJ'],
    'adv': ['ADV'],
    'clb': ['PUNCT', 'SYM'],
    'det': ['DET', 'NUM'],
    'konj': ['CONJ'],
    'interj': ['INTJ'],
    'inf-merke': ['PART'],
    'prep': ['ADP', 'ADV'],
    'pron': ['PRON'],
    '<komma>': ['PUNCT'],
    'sbu': ['SCONJ'],
    '<strek>': ['PUNCT'],
    'subst': ['NOUN', 'PROPN'],
    '<anf>': ['PUNCT'],
    '<parentes-slutt>': ['PUNCT'],
    '<parentes-beg>': ['PUNCT'],
    'symb': ['SYM'],
    'ukjent': ['X'],
    'verb': ['AUX', 'VERB'],
    # 'ufl': ['ADP'] # We need to fix this
}

def pos(text):
    return pos_dict.get(text, [text])

posent_dict = {
    'APP': 'appos',
    'FSUBJ': 'expl',
    'FOBJ': 'expl',
    'FSPRED': 'acl',
    'FOPRED': 'acl',
    'FRAG': 'root',
    'IOBJ': 'iobj',
    'OPRED': 'xcomp',
    'INTERJ': 'discourse',
    'KONJ': 'cc',
    'KOORD': 'conj',
    'KOORD-ELL': 'remnant',
    'IP': 'punct',
    'IK': 'punct',
    'PAR': 'parataxis',
    'SPRED': 'xcomp',
    'UKJENT': 'goeswith',
}

def posent(text):
    return posent_dict.get(text, text)

morph_dict = {
    'mask': 'Gender=Masc',
    'fem': 'Gender=Fem',
    'nøyt': 'Gender=Neut',

    'ent': 'Number=Sing',
    'fl':  'Number=Plur',
    'be': 'Definite=Def',
    'ub': 'Definite=Ind',
    # pres,pret Mood=Ind, Tense=Pres,Past, VerbForm=Fin # Can also be ignored
    'perf-part': 'VerbForm=Part',
    # 'imp': 'Mood=Imp|VerbForm=Fin' # Can be ignored for this use case
    'pass': 'Voice=Pass',
    'inf': 'VerbForm=Inf',
    '1': 'Person=1',
    '2': 'Person=2',
    '3': 'Person=3',
    'nom': 'Case=Nom',
    'akk': 'Case=Acc',
    'gen': 'Case=Gen',
    'pos': 'Degree=Pos',
    'komp': 'Degree=Cmp',
    'sup': 'Degree=Sup',
    'hum': 'Animacy=Anim',
    'pers': 'PronType=Prs',
    'dem': 'PronType=Dem',
    'sp': 'PronType=Int',
    'res': 'PronType=Rcp',
    'poss': 'Poss=Yes',
    'refl': 'Refl=Yes',
}

def morph(text):
    return morph_dict.get(text, text)
