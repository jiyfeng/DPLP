## featselection.py
## Author: Yangfeng Ji
## Date: 02-23-2015
## Time-stamp: <yangfeng 02/23/2015 12:26:05>

from scipy.stats import entropy
from numpy import log, array
from operator import itemgetter

class FeatureSelection(object):
    """ Feature selection module
    """
    def __init__(self, topn, method='frequency'):
        """ Initialization
        """
        self.method = method
        self.topn = topn


    def select(self, vocab, freqtable):
        """ Select features via some criteria

        :type vocab: dict
        :param vocab: feature vocab

        :type freqtable: 2-D numpy.array
        :param freqtable: frequency table with rows as features,
                          columns as frequency values
        """
        if self.method == 'frequency':
            valvocab = self.frequency(vocab, freqtable)
        elif self.method == 'entropy':
            valvocab = self.entropy(vocab, freqtable)
        elif self.method == 'freq-entropy':
            valvocab = self.freq_entropy(vocab, freqtable)
        else:
            raise KeyError("Unrecognized method")
        newvocab = self.rank(valvocab)
        return newvocab


    def rank(self, valvocab):
        """ Rank all features and take top-n features

        :type valvocab: dict
        :param valvocab: {feature:value}
        """
        vocab = {}
        sorted_vals = sorted(valvocab.items(), key=itemgetter(1))
        sorted_vals = sorted_vals[::-1]
        for (idx, item) in enumerate(sorted_vals):
            if idx >= self.topn:
                break
            vocab[item[0]] = idx
        return vocab


    def frequency(self, vocab, freqtable):
        """ Compute frequency values of features
        """
        valvocab = {}
        for (feat, idx) in vocab.iteritems():
            valvocab[feat] = freqtable[idx,:].sum()
        return valvocab


    def entropy(self, vocab, freqtable):
        """
        """
        valvocab = {}
        for (feat, idx) in vocab.iteritems():
            freq = freqtable[idx,:]
            valvocab[feat] = 1/(entropy(freq)+1e-3)
        return valvocab


    def freq_entropy(self, vocab, freqtable):
        """
        """
        valvocab = {}
        freqvocab = self.frequency(vocab, freqtable)
        entvocab = self.entropy(vocab, freqtable)
        for feat in vocab.iterkeys():
            freq = freqvocab[feat]
            ent = freqvocab[feat]
            valvocab[feat] = log(freq+1e-3)*(ent + 1e-3)
        return valvocab


def test():
    vocab = {'hello':0, 'data':1, 'computer':2}
    freqtable = [[23,23,23,23],[23,1,4,5], [1,34,1,1]]
    freqtable = array(freqtable)
    fs = FeatureSelection(topn=2, method='freq-entropy')
    newvocab = fs.select(vocab, freqtable)
    print newvocab


if __name__ == '__main__':
    test()
