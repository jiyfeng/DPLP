## buildmodel.py
## Author: Yangfeng Ji
## Date: 05-03-2015
## Time-stamp: <yangfeng 05/03/2015 05:38:04>

"""
Train a segmentation model
"""

from model.classifier import Classifier
from cPickle import load
import gzip

def main(ftrain, fdev=None, fmodel='model/model.pickle.gz'):
    # Load data
    print 'Loading training data ...'
    data = load(gzip.open(ftrain))
    M, labels = data['data'], data['labels']
    # Load dev data
    if fdev is not None:
        print 'Loading dev data ...'
        devdata = load(gzip.open(fdev))
        devM, devlabels = devdata['data'], devdata['labels']
    else:
        devM, devlabels = None, None
    # Training with specified parameters
    print 'Training ...'
    clf = Classifier()
    clf.train(M, labels, devM, devlabels)
    clf.savemodel(fmodel)

