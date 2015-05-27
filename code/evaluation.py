## evaluation.py
## Author: Yangfeng Ji
## Date: 08-29-2014
## Time-stamp: <yangfeng 02/23/2015 17:34:38>

""" RST parsing evaluation. 
"""

import numpy

class Performance(object):
    def __init__(self, percision, recall):
        self.percision = percision
        self.recall = recall

class Metrics(object):
    def __init__(self, levels=['span','nuclearity','relation']):
        """ Initialization

        :type levels: list of string
        :param levels: evaluation levels, the possible values are only
                       'span','nuclearity','relation'
        """
        self.levels = levels
        self.span_perf = Performance([], [])
        self.nuc_perf = Performance([], [])
        self.rela_perf = Performance([], [])

    def eval(self, goldtree, predtree):
        """ Evaluation performance on one pair of RST trees

        :type goldtree: RSTTree class
        :param goldtree: gold RST tree

        :type predtree: RSTTree class
        :param predtree: RST tree from the parsing algorithm
        """
        goldbrackets = goldtree.bracketing()
        predbrackets = predtree.bracketing()
        for level in self.levels:
            if level == 'span':
                self._eval(goldbrackets, predbrackets, idx=1)
            elif level == 'nuclearity':
                self._eval(goldbrackets, predbrackets, idx=2)
            elif level == 'relation':
                self._eval(goldbrackets, predbrackets, idx=3)
            else:
                raise ValueError("Unrecognized evaluation level: {}".format(level))

    def _eval(self, goldbrackets, predbrackets, idx):
        """ Evaluation on each discourse span
        """
        goldspan = [item[:idx] for item in goldbrackets]
        predspan = [item[:idx] for item in predbrackets]
        allspan = [span for span in goldspan if span in predspan]
        p, r = 0.0, 0.0
        for span in allspan:
            if span in goldspan:
                p += 1.0
            if span in predspan:
                r += 1.0
        p /= len(goldspan)
        r /= len(predspan)
        if idx == 1:
            self.span_perf.percision.append(p)
            self.span_perf.recall.append(r)
        elif idx == 2:
            self.nuc_perf.percision.append(p)
            self.nuc_perf.recall.append(r)
        elif idx == 3:
            self.rela_perf.percision.append(p)
            self.rela_perf.recall.append(r)

    def report(self):
        """ Compute the F1 score for different evaluation levels
            and print it out
        """
        for level in self.levels:
            if 'span' == level:
                p = numpy.array(self.span_perf.percision).mean()
                r = numpy.array(self.span_perf.recall).mean()
                f1 = (2 * p * r) / (p + r)
                print 'F1 score on span level is {0:.4f}'.format(f1)
            elif 'nuclearity' == level:
                p = numpy.array(self.nuc_perf.percision).mean()
                r = numpy.array(self.nuc_perf.recall).mean()
                f1 = (2 * p * r) / (p + r)
                print 'F1 score on nuclearity level is {0:.4f}'.format(f1)
            elif 'relation' == level:
                p = numpy.array(self.rela_perf.percision).mean()
                r = numpy.array(self.rela_perf.recall).mean()
                f1 = (2 * p * r) / (p + r)
                print 'F1 score on relation level is {0:.4f}'.format(f1)
            else:
                raise ValueError("Unrecognized evaluation level")
