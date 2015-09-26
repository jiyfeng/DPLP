## sample.py
## Author: Yangfeng Ji
## Date: 05-02-2015
## Time-stamp: <yangfeng 05/03/2015 09:06:01>

""" Create training examples from a collection of documents
"""

from collections import defaultdict
from feature import FeatureGenerator
from scipy.sparse import lil_matrix, coo_matrix
from util import *

class SampleGenerator(object):
    def __init__(self, vocab):
        """ Initialization
        """
        self.vocab = vocab
        self.fg = FeatureGenerator()
        self.featdict = {}
        self.labels = []

    def build(self, doc):
        """ Build training examples from ONE doc
        """
        N = len(self.featdict)
        index = 0
        featdct = self.fg.extract(doc)
        for (gidx, featlist) in featdct.iteritems():
            self.featdict[N+index] = featlist
            if doc.tokendict[gidx].boundary is not None:
                # No boundary indicator
                if doc.tokendict[gidx].boundary:
                    self.labels.append(1)
                else:
                    self.labels.append(0)
            index += 1
        # print "Read {} samples".format(len(self.featdict))
        # print len(self.featdict), len(self.labels)

    def getmat(self):
        """ Vectorize all elements in featdict
        """
        nRow = len(self.featdict)
        nCol = len(self.vocab)
        Datadict = defaultdict(float)
        Ridx, Cidx, Val = [], [], []
        for ridx in range(nRow):
            # if ridx % 10000 == 0:
            #     print ridx
            for feat in self.featdict[ridx]:
                try:
                    cidx = self.vocab[feat]
                    Datadict[(ridx, cidx)] += 1.0
                except KeyError:
                    pass
        # Convert it to COO format
        for (key, val) in Datadict.iteritems():
            Ridx.append(key[0])
            Cidx.append(key[1])
            Val.append(val)
        M = coo_matrix((Val, (Ridx,Cidx)), shape=(nRow,nCol))
        # print 'Dim of matrix: {}'.format(M.shape)
        return (M, self.labels)
