## data.py
## Author: Yangfeng Ji
## Date: 09-13-2014
## Time-stamp: <yangfeng 09/24/2015 15:47:28>

""" Construct data for training/dev/test data.
Following three steps:
1, build data
2, build vocab (optional, not necessary if vocabs are given)
3, build matrix
4, save/get matrix
5, save/get vocabs (optional, necessary if new)
"""

from util import *
from tree import RSTTree
from featselection import FeatureSelection
from collections import defaultdict
from scipy.sparse import lil_matrix, coo_matrix
from cPickle import dump, load
import os, numpy, gzip

class Data(object):
    def __init__(self, vocab={}, labelmap={}, bcvocab=None,
                 withdp=False,
                 fdpvocab=None, fprojmat=None):
        """ Initialization

        :type vocab: dict
        :param vocab: collections of {feature:index}

        :type labelmap: dict
        :param labelmap: collections of {label:index}
        """
        self.vocab, self.labelmap = vocab, labelmap
        self.bcvocab = bcvocab
        self.actionlist = []
        self.samplelist = []
        self.M, self.L = None, None
        self.withdp = withdp
        self.dpvocab, self.projmat = None, None
        if withdp:
            print 'Loading projection matrix ...'
            with gzip.open(fdpvocab) as fin:
                self.dpvocab = load(fin)
            with gzip.open(fprojmat) as fin:
                self.projmat = load(fin)
        print 'Finish initializing Data'


        
    def builddata(self, rpath):
        """ Build a list of feature list from a given path

        :type path: string
        :param path: data path, where all data files are saved
        """
        # Read RST tree file
        files = [os.path.join(rpath, fname) for fname in os.listdir(rpath) if fname.endswith('.dis')]
        for fdis in files:
            print 'Processing data from file: {}'.format(fdis)
            fmerge = fdis.replace('.dis', '.merge')
            rst = RSTTree(fdis, fmerge)
            rst.build()
            actionlist, samplelist = rst.generate_samples(self.bcvocab)
            self.actionlist += actionlist
            self.samplelist += samplelist
        

    def buildmatrix(self):
        """ Read the results from builddata, and construct
            data matrix
        """
        self.nR, self.nC = len(self.samplelist), len(self.vocab)
        if self.withdp:
            nlatent = self.projmat.shape[1]
            self.nC += (3 * nlatent)
        self.M, self.L = [], []
        for (sidx, sample) in enumerate(self.samplelist):
            label = action2label(self.actionlist[sidx])
            lidx = self.labelmap[label]
            vec = vectorize(sample, self.vocab,
                            self.dpvocab, self.projmat)
            self.L.append(lidx)
            vec = lil_matrix(vec)
            rows, cols = vec.nonzero()
            rows, cols = list(rows), list(cols)
            for (row, col) in zip(rows, cols):
                val = vec[row, col]
                self.M.append((sidx, col, val))


    def buildvocab(self, topn):
        """ Build dict from the current data

        :type topn: int
        :param topn: threshold for feature selection
        """
        featcounts, vocab = {}, {}
        for (action, sample) in zip(self.actionlist, self.samplelist):
            label = action2label(action)
            for feat in sample:
                if feat[0] == 'DisRep':
                    # Skip the features for distributional
                    # representation
                    continue
                try:
                    tmp = vocab[feat]
                except KeyError:
                    featcounts[feat] = defaultdict(float)
                    nvocab = len(vocab)
                    vocab[feat] = nvocab
                featcounts[feat][label] += 1.0
            # Create label mapping
            try:
                labelindex = self.labelmap[label]
            except KeyError:
                nlabel = len(self.labelmap)
                self.labelmap[label] = nlabel
        # Construct freqtable
        nrows, ncols = len(featcounts), len(self.labelmap)
        freqtable = numpy.zeros((nrows, ncols))
        for (feat, nrow) in vocab.iteritems():
            for (label, ncol) in self.labelmap.iteritems():
                freqtable[nrow, ncol] = featcounts[feat][label]
        # Feature selection
        fs = FeatureSelection(topn=topn, method='frequency')
        print 'Original vocab size: {}'.format(len(vocab))
        self.vocab = fs.select(vocab, freqtable)
        

    def savematrix(self, fdata, flabel):
        """ Save matrix into file

        :type fname: string
        :param fname: 
        """
        print 'Save data into: {}'.format(fdata)
        with open(fdata, 'w') as fout:
            line = str(self.nR) + "\t" + str(self.nC) + "\n"
            fout.write(line)
            for t in self.M:
                line = str(t[0]) + "\t" + str(t[1]) + "\t"
                line += str(t[2]) + "\n"
                fout.write(line)
        with open(flabel, 'w') as fout:
            for item in self.L:
                line = str(item) + '\n'
                fout.write(line)
        print 'Done with data saving'


    def loadmatrix(self, fdata, flabel):
        """
        """
        rows, cols, vals = [], [], []
        with open(fdata) as fin:
            items = fin.readline().strip().split('\t')
            nrows, ncols = int(items[0]), int(items[1])
            for line in fin:
                items = line.strip().split('\t')
                rows.append(int(items[0]))
                cols.append(int(items[1]))
                vals.append(float(items[2]))
        if self.withdp:
            nlatent = self.projmat.shape[1]
            ncols = ncols + (3 * nlatent)
        # Create matrix
        M = coo_matrix((vals, (rows, cols)), shape=(nrows, ncols))
        # Read labels
        labels = open(flabel).read().split('\n')
        if len(labels[-1]) == 0:
            labels.pop()
        labels = map(int, labels)
        print 'Load data matrix with shape: {}'.format(M.shape)
        print 'Load {} labels'.format(len(labels))
        return M, labels
                

    def getvocab(self):
        """ Get feature vocab and label mapping
        """
        return self.vocab


    def getrelamap(self):
        """ Get relation map
        """
        return self.relamap


    def getmatrix(self):
        """ Get data matrix and labels
        """
        return (self.M, self.L)
        

    def savevocab(self, fname):
        """ Save vocab into file

        :type fname: string
        :param fname: 
        """
        if not fname.endswith('.gz'):
            fname += '.gz'
        D = {'vocab':self.vocab, 'labelidxmap':self.labelmap}
        with gzip.open(fname, 'w') as fout:
            dump(D, fout)
        print 'Save vocab into file: {}'.format(fname)


    def loadvocab(self, fname):
        pass


def test():
    rpath = "../data/training/"
    data = Data()
    data.builddata(rpath)
    data.buildvocab(thresh=1)
    data.buildmatrix()
    data.savematrix("tmp-data.pickle.gz")
    data.savevocab("tmp-vocab.pickle.gz")


if __name__ == '__main__':
    test()
    
