## docreader.py
## Author: Yangfeng Ji
## Date: 02-14-2015
## Time-stamp: <yangfeng 02/19/2015 21:01:09>

from datastructure import Token, Doc
from os.path import isfile
import sys

class DocReader(object):
    """ Build one doc instance from *.merge file
    """ 
    def __init__(self):
        """
        """
        self.fmerge = None


    def read(self, fmerge):
        """ Read information from the merge file, and create
            an Doc instance

        :type fmerge: string
        :param fmerge: merge file name
        """
        if not isfile(fmerge):
            raise IOError("File doesn't exist: {}".format(fmerge))
        self.fmerge = fmerge
        gidx, tokendict = 0, {}
        with open(fmerge, 'r') as fin:
            for line in fin:
                line = line.strip()
                if len(line) == 0:
                    continue
                tok = self._parseline(line)
                tokendict[gidx] = tok
                gidx += 1
        # Get EDUs from tokendict
        edudict = self._recoveredus(tokendict)
        doc = Doc()
        doc.tokendict = tokendict
        doc.edudict = edudict
        return doc


    def _parseline(self, line):
        """ Parse one line from *.merge file
        """
        items = line.split("\t")
        tok = Token()
        tok.sidx, tok.tidx = int(items[0]), int(items[1])
        # Without changing the case
        tok.word, tok.lemma = items[2], items[3]
        tok.pos = items[4]
        tok.deplabel = items[5]
        try:
            tok.hidx = int(items[6])
        except ValueError:
            pass
        tok.ner, tok.partialparse = items[7], items[8]
        try:
            tok.eduidx = int(items[9])
        except ValueError:
            print tok.word, self.fmerge
            # sys.exit()
            pass
        return tok


    def _recoveredus(self, tokendict):
        """ Recover EDUs from tokendict
        """
        N, edudict = len(tokendict), {}
        for gidx in range(N):
            token = tokendict[gidx]
            eidx = token.eduidx
            try:
                val = edudict[eidx]
                edudict[eidx].append(gidx)
            except KeyError:
                edudict[eidx] = [gidx]
        return edudict
                

if __name__ == '__main__':
    dr = DocReader()
    fmerge = "../data/training/file1.merge"
    doc = dr.read(fmerge)
    print len(doc.edudict)
