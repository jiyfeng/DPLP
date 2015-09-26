## bcreader.py
## Author: Yangfeng Ji
## Date: 01-27-2015
## Time-stamp: <yangfeng 01/30/2015 22:16:26>

from cPickle import dump
import gzip

def reader(fname):
    bcvocab = {}
    with open(fname, 'r') as fin:
        for line in fin:
            items = line.strip().split('\t')
            bcvocab[items[1]] = items[0]
    return bcvocab


def savevocab(vocab, fname):
    with gzip.open(fname, 'w') as fout:
        dump(vocab, fout)
    print 'Done'


if __name__ == '__main__':
    vocab = reader("./bc-3200.txt")
    savevocab(vocab, "./bc3200.pickle.gz")
