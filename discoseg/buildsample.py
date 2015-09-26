## buildsample.py
## Author: Yangfeng Ji
## Date: 05-03-2015
## Time-stamp: <yangfeng 09/25/2015 15:13:36>

from model.docreader import DocReader
from model.sample import SampleGenerator
from cPickle import load, dump
from os import listdir
from os.path import join
import gzip

def main(rpath, fdata, fvocab):
    """ Create data and dump it into a pickle file
    """
    print 'Load vocab ...'
    vocab = load(gzip.open(fvocab))
    dr = DocReader()
    sg = SampleGenerator(vocab)
    flist = [join(rpath,fname) for fname in listdir(rpath) if fname.endswith('merge')]
    for fname in flist:
        # print "Reading file: {}".format(fname)
        doc = dr.read(fname)
        sg.build(doc)
    M, labels = sg.getmat()
    print 'M.shape = {}, len(labels) = {}'.format(M.shape, len(labels))
    data = {'data':M, 'labels':labels}
    if not fdata.endswith('.pickle.gz'):
        fdata += '.pickle.gz'
    with gzip.open(fdata, 'w') as fout:
        dump(data, fout)
    print 'Save data into file: {}'.format(fdata)
