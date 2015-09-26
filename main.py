## main.py
## Author: Yangfeng Ji
## Date: 02-14-2015
## Time-stamp: <yangfeng 09/25/2015 22:03:48>

from code.readdoc import readdoc
from code.data import Data
from code.model import ParsingModel
from code.util import reversedict
from code.evalparser import evalparser
from cPickle import load
import gzip

WITHDP = False

def createdoc():
    ftrn = "data/sample/trn-doc.pickle.gz"
    rpath = "data/training/"
    readdoc(rpath, ftrn)
    ftst = "data/sample/tst-doc.pickle.gz"
    rpath = "data/test/"
    readdoc(rpath, ftst)


def createtrndata(path="data/training/", topn=10000, bcvocab=None):
    data = Data(bcvocab=bcvocab,
                withdp=WITHDP,
                fdpvocab="data/resources/word-dict.pickle.gz",
                fprojmat="data/resources/projmat.pickle.gz")
    data.builddata(path)
    data.buildvocab(topn=topn)
    data.buildmatrix()
    fdata = "data/sample/trn.data"
    flabel = "data/sample/trn.label"
    data.savematrix(fdata, flabel)
    data.savevocab("data/sample/vocab.pickle.gz")


def trainmodel():
    fvocab = "data/sample/vocab.pickle.gz"
    fdata = "data/sample/trn.data"
    flabel = "data/sample/trn.label"
    D = load(gzip.open(fvocab))
    vocab, labelidxmap = D['vocab'], D['labelidxmap']
    print 'len(vocab) = {}'.format(len(vocab))
    data = Data()
    trnM, trnL = data.loadmatrix(fdata, flabel)
    print 'trnM.shape = {}'.format(trnM.shape)
    idxlabelmap = reversedict(labelidxmap)
    pm = ParsingModel(vocab=vocab, idxlabelmap=idxlabelmap)
    pm.train(trnM, trnL)
    pm.savemodel("model/parsing-model.pickle.gz")


if __name__ == '__main__':
    bcvocab=None
    ## Use brown clsuters
    with gzip.open("resources/bc3200.pickle.gz") as fin:
        print 'Load Brown clusters for creating features ...'
        bcvocab = load(fin)
    ## Create training data
    # createtrndata(path="data/training/", topn=8000, bcvocab=bcvocab)
    ## Train model
    # trainmodel()
    ## Evaluate model on the RST-DT test set
    evalparser(path="data/test/", report=True, 
               bcvocab=bcvocab, draw=False,
               withdp=WITHDP,
               fdpvocab="data/resources/word-dict.pickle.gz",
               fprojmat="data/resources/projmat.pickle.gz")
