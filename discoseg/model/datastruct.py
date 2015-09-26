## datastruct.py
## Author: Yangfeng Ji
## Date: 05-02-2015
## Time-stamp: <yangfeng 05/03/2015 02:41:02>

""" Data structure
"""


class Token(object):
    def __init__(self):
        """ Initialization

        :type sidx: string
        :param sidx: sentence index

        :type tidx: string
        :param tidx: token index (within sent)

        :type word: string
        :param word: token itself

        :type pos: string
        :param pos: POS tag

        :type partial_parse: string
        :param partial_parse: partial parse tree

        :type mentioninfo: string
        :param mentioninfo: last column of the OntoNotes format

        :type gidx: string
        :param gidx: golbal token index
        """
        self.sidx, self.tidx = None, None
        self.word, self.lemma = None, None
        self.pos = None
        self.hidx, self.deplabel = None, None
        self.partialparse, self.ner =None, None
        self.eduidx, self.boundary = None, None
        self.gidx, self.send = None, None

        
class Doc(object):
    def __init__(self, tokendict):
        """ Doc
        """
        self.tokendict = tokendict
        # Anything else?
