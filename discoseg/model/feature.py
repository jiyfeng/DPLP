## feature.py
## Author: Yangfeng Ji
## Date: 05-01-2015
## Time-stamp: <yangfeng 05/03/2015 03:51:18>

""" Feature extraction for discourse segmentation
"""

class FeatureGenerator(object):
    def __init__(self):
        """ Initialization for feature extraction
        """
        pass

    def extract(self, doc):
        """ For each token, extract its features
        """
        featdict = {}
        tokendict = doc.tokendict
        N = len(tokendict)
        for n in range(N):
            gidx = tokendict[n].gidx
            feat = self._token_feat(tokendict, n)
            featdict[gidx] = feat
        return featdict
    
    def _token_feat(self, tokendict, n):
        """ Features for one token
        """
        feat = []
        # Basic features (from token itself)
        token = tokendict[n]
        feat.append(('Current-Word', token.word))
        feat.append(('Current-POS', token.pos))
        feat.append(('Current-DepLabel', token.deplabel))
        # Direction to its head
        if token.hidx is not None:
            if token.hidx < token.tidx:
                feat.append(('Head-Direction', 'Left'))
            else:
                feat.append(('Head-Direction', 'Right'))
        else:
            feat.append(('Head-Direction', None))
        # Previous first word
        try:
            prevtok = tokendict[n-1]
        except KeyError:
            prevtok = None
        if prevtok is not None:
            feat.append(('Prev1-Word', prevtok.word))
            feat.append(('Prev1-POS', prevtok.pos))
            feat.append(('Prev1-DepLabel', prevtok.deplabel))
        # Previous second word
        try:
            prev2tok = tokendict[n-2]
        except KeyError:
            prev2tok = None
        if prev2tok is not None:
            feat.append(('Prev2-Word', prev2tok.word))
            feat.append(('Prev2-POS', prev2tok.pos))
            feat.append(('Prev2-DepLabel', prev2tok.deplabel))
        # Next first word
        try:
            nexttok = tokendict[n+1]
        except KeyError:
            nexttok = None
        if nexttok is not None:
            feat.append(('Next1-Word',nexttok.word))
            feat.append(('Next1-POS',nexttok.pos))
            feat.append(('Next1-DepLabel',nexttok.deplabel))
        # Next second word
        try:
            next2tok = tokendict[n+2]
        except KeyError:
            next2tok = None
        if next2tok is not None:
            feat.append(('Next2-Word',next2tok.word))
            feat.append(('Next2-POS',next2tok.pos))
            feat.append(('Next2-DepLabel',next2tok.deplabel))
        # Dependency-tree related features
        # TODO
        return feat
