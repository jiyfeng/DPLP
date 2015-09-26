## tree.py
## Author: Yangfeng Ji
## Date: 08-29-2014
## Time-stamp: <yangfeng 09/24/2015 15:45:12>

""" Any operation about an RST tree should be here
1, Build general/binary RST tree from annotated file
2, Binarize a general RST tree to the binary form
3, Generate bracketing sequence for evaluation
4, Write an RST tree into file (not implemented yet)
5, Generate Shift-reduce parsing action examples
6, Get all EDUs from the RST tree
- YJ
"""

from datastructure import *
from buildtree import *
from docreader import DocReader
from feature import FeatureGenerator
from parser import SRParser
from util import extractrelation
from os.path import isfile


class RSTTree(object):
    def __init__(self, fdis=None, fmerge=None):
        """ Initialization
            There are two different ways to initialize a Tree
            instance: (1) read the RST annotation *.dis, or
            (2) directly assign another Tree instance to it

        :type text: string
        :param text: dis file content
        """
        self.fdis, self.fmerge = fdis, fmerge
        self.binary = True
        self.tree, self.doc = None, None


    def asign_tree(self, tree):
        """ Asign a tree instance from external resource
        """
        self.tree = tree


    def build(self):
        """ Build BINARY RST tree
        """
        text = open(self.fdis).read()
        # Build RST as annotation
        self.tree = buildtree(text)
        # Binarize it
        self.tree = binarizetree(self.tree)
        # Read doc file
        if isfile(self.fmerge):
            dr = DocReader()
            self.doc = dr.read(self.fmerge)
        else:
            raise IOError("File doesn't exist: {}".format(self.fmerge))
        # Prop information from doc on the binarized RST tree
        self.tree = backprop(self.tree, self.doc)
            

    def parse(self):
        """ Get parse tree in string format

            For visualization, use nltk.tree:
            from nltk.tree import Tree
            t = Tree.fromstring(parse)
            t.draw()
        """
        parse = getparse(self.tree, "")
        return parse


    def bracketing(self):
        """ Generate brackets according an Binary RST tree
        """
        nodelist = postorder_DFT(self.tree, [])
        nodelist.pop() # Remove the root node
        brackets = []
        for node in nodelist:
            relation = extractrelation(node.relation)
            b = (node.eduspan, node.prop, relation)
            brackets.append(b)
        return brackets


    def generate_samples(self, bcvocab):
        """ Generate samples from an binary RST tree

        :type bcvocab: dict
        :param bcvocab: brown clusters of words
        """
        # Sample list
        samplelist = []
        # Parsing action
        actionlist = decodeSRaction(self.tree)
        # Initialize queue and stack
        queue = getedunode(self.tree)
        stack = []
        # Start simulating the shift-reduce parsing
        for action in actionlist:
            # Generate features
            fg = FeatureGenerator(stack, queue, self.doc, bcvocab)
            features = fg.features()
            samplelist.append(features)
            # Change status of stack/queue
            sr = SRParser(stack, queue)
            sr.operate(action)
            # stack, queue = sr.getstatus()
        return (actionlist, samplelist)


    def getedutext(self):
        """ Get all EDU text here
        """
        edunodelist = getedunode(self.tree)
        texts = []
        for node in edunodelist:
            texts.append(node.text)
        return texts


    def gettree(self):
        """ Get the RST tree
        """
        return self.tree

def test():
    fdis = "../data/training/file2.dis"
    fmerge = "../data/training/file2.merge"
    rst = RSTTree(fdis, fmerge)
    rst.build()
    strparse = rst.parse()
    print strparse
    # actionlist, samplelist = rst.generate_samples()
    # print actionlist
    # print samplelist
    # for (action, sample) in zip(actionlist, samplelist):
    #     print action
    # print rst.bracketing()



if __name__ == '__main__':
    test()
