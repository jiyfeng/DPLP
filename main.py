## main.py
## Author: Yangfeng Ji
## Date: 02-14-2015
## Time-stamp: <yangfeng 03/02/2015 17:32:12>

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


def createtrndata(path="data/training/"):
    data = Data(withdp=WITHDP,
        fdpvocab="data/resources/word-dict.pickle.gz",
        fprojmat="data/resources/projmat.pickle.gz")
    data.builddata(path)
    data.buildvocab(topn=15000)
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
    createtrndata(path="data/training/")
    trainmodel()
    evalparser(path="data/test/", report=True, withdp=WITHDP,
        fdpvocab="data/resources/word-dict.pickle.gz",
        fprojmat="data/resources/projmat.pickle.gz")
