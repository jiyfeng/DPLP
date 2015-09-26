## buildedu.py
## Author: Yangfeng Ji
## Date: 05-03-2015
## Time-stamp: <yangfeng 09/25/2015 15:35:08>

from os import listdir
from os.path import join, basename
from model.classifier import Classifier
from model.docreader import DocReader
from model.sample import SampleGenerator
from cPickle import load
import gzip


def main(fmodel, fvocab, rpath, wpath):
    clf = Classifier()
    dr = DocReader()
    clf.loadmodel(fmodel)
    flist = [join(rpath,fname) for fname in listdir(rpath) if fname.endswith('conll')]
    vocab = load(gzip.open(fvocab))
    for (fidx, fname) in enumerate(flist):
        print "Processing file: {}".format(fname)
        doc = dr.read(fname, withboundary=False)
        sg = SampleGenerator(vocab)
        sg.build(doc)
        M, _ = sg.getmat()
        predlabels = clf.predict(M)
        doc = postprocess(doc, predlabels)
        writedoc(doc, fname, wpath)


def postprocess(doc, predlabels):
    """ Assign predlabels into doc
    """
    tokendict = doc.tokendict
    for gidx in tokendict.iterkeys():
        if predlabels[gidx] == 1:
            tokendict[gidx].boundary = True
        else:
            tokendict[gidx].boundary = False
        if tokendict[gidx].send:
            tokendict[gidx].boundary = True
    return doc


# def writedoc(doc, fname, wpath):
#     """ Write doc into a file with the CoNLL-like format
#     """
#     tokendict = doc.tokendict
#     N = len(tokendict)
#     fname = basename(fname) + '.edu'
#     fname = join(wpath, fname)
#     eduidx = 0
#     with open(fname, 'w') as fout:
#         for gidx in range(N):
#             fout.write(str(eduidx) + '\n')
#             if tokendict[gidx].boundary:
#                 eduidx += 1
#             if tokendict[gidx].send:
#                 fout.write('\n')
#     print 'Write segmentation: {}'.format(fname)


def writedoc(doc, fname, wpath):
    """ Write file
    """
    tokendict = doc.tokendict
    N = len(tokendict)
    fname = basename(fname).replace(".conll", ".merge")
    fname = join(wpath, fname)
    eduidx = 1
    with open(fname, 'w') as fout:
        for gidx in range(N):
            tok = tokendict[gidx]
            line = str(tok.sidx) + "\t" + str(tok.tidx) + "\t"
            line += tok.word + "\t" + tok.lemma + "\t" 
            line += tok.pos + "\t" + tok.deplabel + "\t" 
            line += str(tok.hidx) + "\t" + tok.ner + "\t"
            line += tok.partialparse + "\t" + str(eduidx) + "\n"
            fout.write(line)
            # Boundary
            if tok.boundary:
                eduidx += 1
            if tok.send:
                fout.write("\n")
