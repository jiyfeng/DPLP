## readdoc.py
## Author: Yangfeng Ji
## Date: 05-02-2015
## Time-stamp: <yangfeng 09/25/2015 15:18:23>

from datastruct import *
from util import isnumber

""" Read *.merge file
"""

class DocReader(object):
    def __init__(self):
        """ Initialization
        """
        pass

    def read(self, fconll, withboundary=True):
        """
        """
        fin = open(fconll, 'r')
        gidx, tokendict = 0, {}
        for line in fin:
            line = line.strip()
            if len(line) == 0:
                continue
            token = self._parseline(line, gidx)
            tokendict[gidx] = token
            gidx += 1
        # print tokendict
        # Assign sentence boundary
        tokendict = self._sentboundary(tokendict)
        # Assign EDU boundary
        if withboundary:
            tokendict = self._postprocess(tokendict)
        doc = Doc(tokendict)
        return doc


    def _sentboundary(self, tokendict):
        """ Assign sentence boundary
        """
        N = len(tokendict)
        for n in range(N):
            if (n+1) == N:
                tokendict[n].send = True
            elif (tokendict[n].sidx < tokendict[n+1].sidx):
                tokendict[n].send = True
        return tokendict

    def _postprocess(self, tokendict):
        """ Post-processing, includes:
        1, Identify discourse boundary
        """
        N = len(tokendict)
        for n in range(N):
            if (n+1) == N:
                tokendict[n].boundary = True
            elif (tokendict[n].eduidx < tokendict[n+1].eduidx):
                tokendict[n].boundary = True
            else:
                tokendict[n].boundary = False
        return tokendict
            
        

    def _parseline(self, line, gidx):
        """ Parse one line

        :type line: string
        :param line: one line from CoNLL-like format

        :type gidx: int
        :param gidx: global token index
        """
        items = line.strip().split('\t')
        tok = Token()
        tok.sidx, tok.tidx = int(items[0]), int(items[1])
        tok.word, tok.lemma = items[2], items[3]
        tok.pos, tok.deplabel = items[4], items[5]
        if isnumber(items[6]):
            tok.hidx = int(items[6])
        else:
            # No head word
            tok.hidx = None
        tok.ner = items[7]
        try:
            tok.partialparse = items[8]
        except IndexError:
            pass
        if len(items) == 10:
            tok.eduidx = int(items[9])
        elif (len(items) == 9) or (len(items) == 8):
            pass
        else:
            raise ValueError("Unrecognized format")
        tok.gidx = gidx
        return tok
        
