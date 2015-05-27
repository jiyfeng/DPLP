## evalparser.py
## Author: Yangfeng Ji
## Date: 11-05-2014
## Time-stamp: <yangfeng 03/02/2015 15:15:38>

from model import ParsingModel
from tree import RSTTree
from docreader import DocReader
from evaluation import Metrics
from os import listdir
from os.path import join as joinpath


def parse(pm, doc):
    """ Parse one document using the given parsing model

    :type pm: ParsingModel
    :param pm: an well-trained parsing model

    :type fedus: string
    :param fedus: file name of an document (with segmented EDUs) 
    """
    pred_rst = pm.sr_parse(doc)
    return pred_rst


def writebrackets(fname, brackets):
    """ Write the bracketing results into file
    """
    print 'Writing parsing results into file: {}'.format(fname)
    with open(fname, 'w') as fout:
        for item in brackets:
            fout.write(str(item) + '\n')


def evalparser(path='./examples', report=False, withdp=False,
               fdpvocab=None, fprojmat=None):
    """ Test the parsing performance

    :type path: string
    :param path: path to the evaluation data

    :type report: boolean
    :param report: whether to report (calculate) the f1 score
    """
    # ----------------------------------------
    # Load the parsing model
    print 'Load parsing model ...'
    pm = ParsingModel(withdp=withdp,
        fdpvocab=fdpvocab, fprojmat=fprojmat)
    pm.loadmodel("model/parsing-model.pickle.gz")
    # ----------------------------------------
    # Evaluation
    met = Metrics(levels=['span','nuclearity','relation'])
    # ----------------------------------------
    # Read all files from the given path
    doclist = [joinpath(path, fname) for fname in listdir(path) if fname.endswith('.merge')]
    for fmerge in doclist:
        # ----------------------------------------
        # Read *.merge file
        dr = DocReader()
        doc = dr.read(fmerge)
        # ----------------------------------------
        # Parsing
        pred_rst = pm.sr_parse(doc)
        # Get brackets from parsing results
        pred_brackets = pred_rst.bracketing()
        fbrackets = fmerge.replace('.merge', '.brackets')
        # Write brackets into file
        writebrackets(fbrackets, pred_brackets)
        # ----------------------------------------
        # Evaluate with gold RST tree
        if report:
            fdis = fmerge.replace('.merge', '.dis')
            gold_rst = RSTTree(fdis, fmerge)
            gold_rst.build()
            gold_brackets = gold_rst.bracketing()
            met.eval(gold_rst, pred_rst)
    if report:
        met.report()
