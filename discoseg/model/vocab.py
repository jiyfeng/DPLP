## vocab.py
## Author: Yangfeng Ji
## Date: 05-02-2015
## Time-stamp: <yangfeng 05/03/2015 03:45:40>

""" Build vocab
1, read each document for creating the feature list
2, collecting all features with their frequency
3, creating vocab with feature selection
"""

from collections import defaultdict
from feature import FeatureGenerator
from cPickle import dump
import gzip

class VocabGenerator(object):
    def __init__(self, thresh=20, topn=100):
        """ Initialization
        """
        self.vocab = {}
        self.features = defaultdict(float)
        self.thresh = thresh
        self.topn = topn
        self.fg = FeatureGenerator()

        
    def build(self, doc):
        """ Extract features for a given doc

        :type doc: Doc instance
        :param doc: 
        """
        featdict = self.fg.extract(doc)
        for (idx, featlist) in featdict.iteritems():
            for feat in featlist:
                self.features[feat] += 1.0

    
    def select(self):
        """ Select top-n features according to frequency
        """
        pass


    def filter(self):
        """ Filter out low-frequency features with thresh
        """
        index = 0
        for (feat, freq) in self.features.iteritems():
            if freq >= self.thresh:
                self.vocab[feat] = index
                index += 1

    def getvocab(self):
        """ Return vocab
        """
        if len(self.vocab) == 0:
            raise ValueError("Empty vocab")
        return self.vocab

    def savevocab(self, fvocab):
        """ Dump vocab into a pickle file
        """
        if not fvocab.endswith('pickle.gz'):
            fvocab += 'pickle.gz'
        fout = gzip.open(fvocab, 'w')
        if len(self.vocab) == 0:
            raise ValueError("Empty vocab")
        dump(self.vocab, fout)
        print "Save vocab into file: {}".format(fvocab)
