## util.py
## Author: Yangfeng Ji
## Date: 09-13-2014
## Time-stamp: <yangfeng 09/25/2015 16:07:29>

from scipy.sparse import lil_matrix, hstack
from sklearn.preprocessing import normalize
from nltk import Tree
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget

def label2action(label):
    """ Transform label to action
    """
    items = label.split('-')
    if len(items) == 1:
        action = (items[0], None, None)
    elif len(items) == 3:
        action = tuple(items)
    elif len(items) > 3:
        relalabel = '-'.join(items[2:])
        action = tuple((items[0], items[1], relalabel))
    else:
        raise ValueError("Unrecognized label: {}".format(label))
    return action


def action2label(action):
    """ Transform action into label
    """
    if action[0] == 'Shift':
        label = action[0]
    elif action[0] == 'Reduce':
        label = '-'.join(list(action))
    else:
        raise ValueError("Unrecognized parsing action: {}".format(action))
    return label


def vectorize(features, vocab, dpvocab=None, projmat=None):
    """ Transform a feature list into a numeric vector
        with a given vocab

    :type dpvocab: dict
    :param dpvocab: vocab for distributional representation

    :type projmat: scipy.lil_matrix
    :param projmat: projection matrix for disrep
    """
    vec = lil_matrix((1, len(vocab)))
    if (dpvocab is not None) and (projmat is not None):
        withdp = True
        ndpvocab = len(dpvocab)
        dpvec1 = lil_matrix((1, ndpvocab))
        dpvec2 = lil_matrix((1, ndpvocab))
        dpvec3 = lil_matrix((1, ndpvocab))
    else:
        withdp = False
    for feat in features:
        try:
            fidx = vocab[feat]
            vec[0, fidx] += 1.0
        except KeyError:
            pass
        if (withdp == True) and (feat[0] == 'DisRep'):
            tag, word = feat[1], feat[2]
            try:
                widx = dpvocab[word]
                if tag == 'Top1Span':
                    dpvec1[0, widx] += 1.0
                elif tag == 'Top2Span':
                    dpvec2[0, widx] += 1.0
                elif tag == 'FirstSpan':
                    dpvec3[0, widx] += 1.0
                else:
                    raise ValueError("Error")
            except KeyError:
                widx = None
    # Normalization
    vec = normalize(vec)
    # Projection
    if withdp:
        nlat = projmat.shape[1]
        vec_dense = lil_matrix((1, 3*nlat))
        v1 = dpvec1.dot(projmat)
        v2 = dpvec2.dot(projmat)
        v3 = dpvec3.dot(projmat)
        vec_dense[0, 0:nlat] = normalize(v1)
        vec_dense[0, nlat:(2*nlat)] = normalize(v2)
        vec_dense[0, (2*nlat):(3*nlat)] = normalize(v3)
        vec = hstack([vec, vec_dense])
    return vec


def extractrelation(s, level=0):
    """ Extract discourse relation on different level
    """
    items = s.lower().split('-')
    if items[0] == 'same':
        rela = '_'.join(items[:2])
    else:
        rela = items[0]
    return rela


def reversedict(dct):
    """ Reverse the {key:val} in dct to
        {val:key}
    """
    # print labelmap
    newmap = {}
    for (key, val) in dct.iteritems():
        newmap[val] = key
    return newmap


def getgrams(text, tokendict):
    """ Generate first one, two words from the token list

    :type text: list of int
    :param text: indices of words with the text span

    :type tokendict: dict of Token (data structure)
    :param tokendict: all tokens in the doc, indexing by the
                      document-level index
    """
    n = len(text)
    grams = []
    # Get lower-case of words
    if n >= 1:
        grams.append(tokendict[text[0]].word.lower())
        grams.append(tokendict[text[-1]].word.lower())
        grams.append(tokendict[text[0]].pos)
        grams.append(tokendict[text[-1]].pos)
    if n >= 2:
        token = tokendict[text[0]].word.lower() + ' ' + tokendict[text[1]].word.lower()
        grams.append(token)
        token = tokendict[text[-2]].word.lower() + ' ' + tokendict[text[-1]].word.lower()
        grams.append(token)
    return grams


def getbc(eduidx, edudict, tokendict, bcvocab, nprefix=5):
    """ Get brown cluster features for tokens

    :type eduidx: int 
    :param eduidx: index of one EDU

    :type edudict: dict
    :param edudict: All EDUs in one dict

    :type tokendict: dict of Token (data structure)
    :param tokendict: all tokens in the doc, indexing by the
                      document-level index

    :type bcvocab: dict {word : braown-cluster-index}
    :param bcvocab: brown clusters

    :type nprefix: int
    :param nprefix: number of prefix we want to keep from 
                    cluster indices
    """
    text = edudict[eduidx]
    bcfeatures = []
    for gidx in text:
        tok = tokendict[gidx].word.lower()
        try:
            bcidx = bcvocab[tok][:nprefix]
            bcfeatures.append(bcidx)
        except KeyError:
            pass
    return bcfeatures


def drawrst(strtree, fname):
    """ Draw RST tree into a file
    """
    if not fname.endswith(".ps"):
        fname += ".ps"
    cf = CanvasFrame()
    t = Tree.fromstring(strtree)
    tc = TreeWidget(cf.canvas(), t)
    cf.add_widget(tc,10,10) # (10,10) offsets
    cf.print_to_file(fname)
    cf.destroy()
