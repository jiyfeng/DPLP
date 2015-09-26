## util.py
## Author: Yangfeng Ji
## Date: 01-19-2015
## Time-stamp: <yangfeng 05/03/2015 04:30:18>

import numpy
from scipy.sparse import lil_matrix, csr_matrix

def isnumber(s):
    """ Is number or not
    """
    try:
        val = int(s)
        return True
    except ValueError:
        return False


def vectorize(feats, vocab):
    # print vocab
    vec = lil_matrix((1,len(vocab)))
    for feat in feats:
        try:
            idx = vocab[feat]
            vec[0,idx] += 1.0
        except KeyError:
            # print feat
            pass
    return vec

