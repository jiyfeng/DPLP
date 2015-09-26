## buildvocab.py
## Author: Yangfeng Ji
## Date: 05-03-2015
## Time-stamp: <yangfeng 05/03/2015 05:03:13>

"""
Build vocab from a collection of documents
"""

from model.vocab import VocabGenerator
from model.docreader import DocReader
from os import listdir
from os.path import join

def main(rpath, thresh, fvocab):
    """ Build vocab and save it into a pickle file
    """
    vg = VocabGenerator(thresh=thresh)
    dr = DocReader()
    flist = [join(rpath,fname) for fname in listdir(rpath) if fname.endswith('merge')]
    for fname in flist:
        print "Reading file: {}".format(fname)
        doc = dr.read(fname)
        vg.build(doc)
    vg.filter()
    vocab = vg.getvocab()
    print "Vocab size = {}".format(len(vocab))
    if not fvocab.endswith('.pickle.gz'):
        fvocab += '.pickle.gz'
    vg.savevocab(fvocab)
    with open('vocab.txt', 'w') as fout:
        for (feat, idx) in vocab.iteritems():
            fout.write(str(feat) + '\t' + str(idx) + '\n')

