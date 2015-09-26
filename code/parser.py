## parser.py
## Author: Yangfeng Ji
## Date: 08-29-2014
## Time-stamp: <yangfeng 09/25/2015 16:40:09>

""" Shift-reduce parser, including following functions
1, Initialize parsing status given a sequence of texts
2, Change the status according to a specific parsing action
3, Get the status of stack/queue
4, Check whether should stop parsing
- YJ
"""

from datastructure import *
from util import *

class SRParser:
    """ It shouldn't be a sub-class of 'object',
        otherwise, it won't work.
        To be clear, being a sub-class of 'object',
        it will make copy of stack and queue, but I
        don't want it works in that way with a purpose.
        - YJ
    """
    def __init__(self, stack, queue):
        """ Initialization
        """
        self.Stack = stack
        self.Queue = queue


    def init(self, doc):
        """ Using text to initialize Queue

        :type doc: Doc instance
        :param doc: 
        """
        if not isinstance(doc, Doc):
            raise ValueError("doc should be an instance of Doc")
        N = len(doc.edudict)
        for idx in range(1, N+1, 1):
            node = SpanNode(prop=None)
            node.text = doc.edudict[idx]
            node.eduspan, node.nucspan = (idx, idx), (idx, idx)
            node.nucedu = idx
            self.Queue.append(node)


    def operate(self, action_tuple):
        """ According to parsing label to modify the status of
            the Stack/Queue

        Need a special exception for parsing error -YJ

        :type action_tuple: tuple (,,)
        :param action_tuple: one specific parsing action,
                             for example: reduce-NS-elaboration
        """
        action, form, relation = action_tuple
        if action == 'Shift':
            if len(self.Queue) == 0:
                raise ActionError("Shift action error")
            node = self.Queue.pop(0)
            self.Stack.append(node)
        elif action == 'Reduce':
            if len(self.Stack) < 2:
                raise ActionError("Reduce action error")
            rnode = self.Stack.pop()
            lnode = self.Stack.pop()
            # Create a new node
            # Assign a value to prop, only when it is someone's
            #   children node
            node = SpanNode(prop=None)
            # Children node
            node.lnode, node.rnode = lnode, rnode
            # Parent node of children nodes
            node.lnode.pnode, node.rnode.pnode = node, node
            # Node text: concatenate two word lists
            node.text = lnode.text + rnode.text
            # EDU span
            node.eduspan = (lnode.eduspan[0],rnode.eduspan[1])
            # Nuc span / Nuc EDU
            node.form = form
            if form == 'NN':
                node.nucspan = (lnode.eduspan[0],rnode.eduspan[1])
                node.nucedu = lnode.nucedu
                node.lnode.prop = "Nucleus"
                node.lnode.relation = relation
                node.rnode.prop = "Nucleus"
                node.rnode.relation = relation
            elif form == 'NS':
                node.nucspan = lnode.eduspan
                node.nucedu = lnode.nucedu
                node.lnode.prop = "Nucleus"
                node.lnode.relation = "span"
                node.rnode.prop = "Satellite"
                node.rnode.relation = relation
            elif form == 'SN':
                node.nucspan = rnode.eduspan
                node.nucedu = rnode.nucedu
                node.lnode.prop = "Satellite"
                node.lnode.relation = relation
                node.rnode.prop = "Nucleus"
                node.rnode.relation = "span"
            else:
                raise ValueError("Unrecognized form: {}".format(form))
            self.Stack.append(node)
            # How about prop? How to update it?
        else:
            raise ValueError("Unrecoginized parsing action: {}".format(action))


    def getstatus(self):
        """ Return the status of the Queue/Stack
        """
        return (self.Stack, self.Queue)


    def endparsing(self):
        """ Whether we should end parsing
        """
        if (len(self.Stack) == 1) and (len(self.Queue) == 0):
            return True
        elif (len(self.Stack) == 0) and (len(self.Queue) == 0):
            raise ParseError("Illegal stack/queue status")
        else:
            return False

    def getparsetree(self):
        """ Get the entire parsing tree
        """
        if (len(self.Stack) == 1) and (len(self.Queue) == 0):
            return self.Stack[0]
        else:
            return None

            
