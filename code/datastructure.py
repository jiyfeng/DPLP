## datastructure.py
## Author: Yangfeng Ji
## Date: 08-29-2013
## Time-stamp: <yangfeng 02/14/2015 00:28:50>

class SpanNode(object):
    """ RST tree node
    """
    def __init__(self, prop):
        """ Initialization of SpanNode

        :type text: string
        :param text: text of this span
        """
        # Text of this span / Discourse relation
        self.text, self.relation = None, None
        # EDU span / Nucleus span (begin, end) index
        self.eduspan, self.nucspan = None, None
        # Nucleus single EDU
        self.nucedu = None
        # Property
        self.prop = prop
        # Children node
        # Each of them is a node instance
        # N-S form (for binary RST tree only)
        self.lnode, self.rnode = None, None
        # Parent node
        self.pnode = None
        # Node list (for general RST tree only)
        self.nodelist = []
        # Relation form: NN, NS, SN
        self.form = None
        

class ParseError(Exception):
    """ Exception for parsing
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class ActionError(Exception):
    """ Exception for illegal parsing action
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Token(object):
    """ Token class
    """
    def __init__(self):
        # Sentence index, token index (within sent)
        self.sidx, self.tidx = None, None
        # Word, Lemma
        self.word, self.lemma = None, None
        # POS tag
        self.pos = None
        # Dependency label, head index
        self.deplabel, self.hidx = None, None
        # NER, Partial parse tree
        self.ner, self.partialparse = None, None
        # EDU index
        self.eduidx = None


class Doc(object):
    """ Document
    """
    def __init__(self):
        # Token dict
        self.tokendict = None
        # EDU dict
        self.edudict = None
        # Relation pair
        self.relapairs = None
