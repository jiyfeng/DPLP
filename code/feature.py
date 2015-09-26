## feature.py
## Author: Yangfeng Ji
## Date: 08-29-2014
## Time-stamp: <yangfeng 09/24/2015 16:21:12>

from util import getgrams, getbc
from cPickle import load
import gzip

class FeatureGenerator(object):
    def __init__(self, stack, queue, doc, bcvocab, nprefix=10):
        """ Initialization of feature generator

        Currently, we only consider the feature generated
        from the top 2 spans from the stack, and the first
        span from the queue. However, you are available to
        use any other information for feature generation.
        - YJ
        
        :type stack: list
        :param stack: list of Node instance

        :type queue: list
        :param queue: list of Node instance

        :type doc: Doc instance
        :param doc: 
        """
        # Predefined variables
        self.npref = nprefix
        # Load Brown clusters
        self.bcvocab = bcvocab
        # -------------------------------------
        self.doc = doc
        # Stack
        if len(stack) >= 2:
            self.top1span, self.top2span = stack[-1], stack[-2]
        elif len(stack) == 1:
            self.top1span, self.top2span = stack[-1], None
        else:
            self.top1span, self.top2span = None, None
        # Queue
        if len(queue) > 0:
            self.firstspan = queue[0]
        else:
            self.firstspan = None
        # Doc length wrt EDUs
        self.doclen = len(self.doc.edudict)


    def features(self):
        """ Main function to generate features
        """
        featlist = []
        ## Status features (Basic features)
        for feat in self.status_features():
            featlist.append(feat)
        ## Lexical features
        for feat in self.lexical_features():
            featlist.append(feat)
        ## Structural features
        for feat in self.structural_features():
            featlist.append(feat)
        ## EDU features
        for feat in self.edu_features():
            featlist.append(feat)
        ## Distributional representation
        for feat in self.distributional_features():
            featlist.append(feat)
        ## Brown clusters
        if self.bcvocab is not None:
            for feat in self.bc_features():
                featlist.append(feat)
        return featlist
            

    def structural_features(self):
        """ Structural features

        TODO: add a upper/lower thresholds
        """
        features = []
        if self.top1span is not None:
            span = self.top1span
            # Span Length wrt EDUs
            edulen1 = span.eduspan[1]-span.eduspan[0]+1
            yield ('Top1-Stack','Length-EDU', edulen1)
            # Distance to the beginning of the document wrt EDUs
            yield ('Top1-Stack','Dist-To-Begin',span.eduspan[0])
            # Distance to the end of the document wrt EDUs
            yield ('Top1-Stack','Dist-To-End',self.doclen-span.eduspan[1])
        if self.top2span is not None:
            span = self.top2span
            edulen2 = span.eduspan[1]-span.eduspan[0]+1
            yield ('Top2-Stack','Length-EDU', edulen2)
            yield ('Top2-Stack','Dist-To-Begin',span.eduspan[0])
            yield ('Top2-Stack','Dist-To-End',self.doclen-span.eduspan[1])
        # if (self.top1span is not None) and (self.top2span is not None):
        #     if edulen1 > edulen2:
        #         yield ('Top-Stack','EDU-Comparison',True)
        #     elif edulen1 < edulen2:
        #         yield ('Top-Stack','EDU-Comparison',False)
        #     else:
        #         yield ('Top-Stack','EDU-Comparison','Equal')
        if self.firstspan is not None:
            span = self.firstspan
            yield ('First-Queue','Dist-To-Begin',span.eduspan[0])
        

    def status_features(self):
        """ Features related to stack/queue status
        """
        # Stack
        if (self.top1span is None) and (self.top2span is None):
            yield ('Stack','Empty')
        elif (self.top1span is not None) and (self.top2span is None):
            yield ('Stack', 'OneElem')
        elif (self.top1span is not None) and (self.top2span is not None):
            yield ('Stack', 'MoreElem')
        else:
            raise ValueError("Unrecognized stack status")
        # Queue
        if (self.firstspan is None):
            yield ('Queue', 'Empty')
        else:
            yield ('Queue', 'NonEmpty')


    def edu_features(self):
        """ Features about EDUs in one text span
        """
        # ---------------------------------------
        # EDU length
        if self.top1span is not None:
            eduspan = self.top1span.eduspan
            yield ('Top1-Stack', 'nEDUs', eduspan[1]-eduspan[0]+1)
        if self.top2span is not None:
            eduspan = self.top2span.eduspan
            yield ('Top1-Stack', 'nEDUs', eduspan[1]-eduspan[0]+1)
        # ---------------------------------------
        # Whether within same sentence
        # Span 1 and 2
        # Last word from span 1, first word from span 2
        try:
            text1, text2 = self.top1span.text, self.top2span.text
            if (self.doc.tokendict[text1[-1]].sidx == self.doc.tokendict[text2[0]].sidx):
                yield ('Top12-Stack', 'SameSent', True)
            else:
                yield ('Top12-Stack', 'SameSent', False)
        except AttributeError:
            yield ('Top12-Stack', 'SameSent', None)
        # Span 1 and top span
        # First word from span 1, last word from span 3
        try:
            text1, text3 = self.top1span.text, self.firstspan.text
            if (self.doc.tokendict[text1[0]].sidx == self.doc.tokendict[text3[-1]].sidx):
                yield ('Stack-Queue', 'SameSent', True)
            else:
                yield ('Stack-Queue', 'SameSent', False)
        except AttributeError:
            yield ('Stack-Queue', 'SameSent', None)


    def lexical_features(self):
        """ Features about tokens in one text span
        """ 
        if self.top1span is not None:
            span = self.top1span
            # yield ('Top1-Stack', 'nTokens', len(span.text))
            grams = getgrams(span.text, self.doc.tokendict)
            for gram in grams:
                yield ('Top1-Stack', 'nGram', gram)
        if self.top2span is not None:
            span = self.top2span
            # yield ('Top2-Stack', 'nTokens', len(span.text))
            grams = getgrams(span.text, self.doc.tokendict)
            for gram in grams:
                yield ('Top2-Stack', 'nGram', gram)
        if self.firstspan is not None:
            span = self.firstspan
            # yield ('First-Queue', 'nTokens', len(span.text))
            grams = getgrams(span.text, self.doc.tokendict)
            for gram in grams:
                yield ('First-Queue', 'nGram', gram)


    def distributional_features(self):
        """ Distributional representation features proposed in
            (Ji and Eisenstein, 2014)
        """
        tokendict = self.doc.tokendict
        if self.top1span is not None:
            eduidx = self.top1span.nucedu
            for gidx in self.doc.edudict[eduidx]:
                word = tokendict[gidx].word.lower()
                yield ('DisRep', 'Top1Span', word)
        if self.top2span is not None:
            eduidx = self.top2span.nucedu
            for gidx in self.doc.edudict[eduidx]:
                word = tokendict[gidx].word.lower()
                yield ('DisRep', 'Top2Span', word)
        if self.firstspan is not None:
            eduidx = self.firstspan.nucedu
            for gidx in self.doc.edudict[eduidx]:
                word = tokendict[gidx].word.lower()
                yield ('DisRep', 'FirstSpan', word)


    def nucleus_features(self):
        """ Feature extract from one single nucleus EDU
        """
        pass

    
    def bc_features(self):
        """ Feature extract from brown clusters
            Features are only extracted from Nucleus EDU !!!!
        """
        tokendict = self.doc.tokendict
        edudict = self.doc.edudict
        if self.top1span is not None:
            eduidx = self.top1span.nucedu
            bcfeatures = getbc(eduidx, edudict, tokendict, 
                               self.bcvocab, self.npref)
            for feat in bcfeatures:
                yield ('BC', 'Top1Span', feat)
        if self.top2span is not None:
            eduidx = self.top2span.nucedu
            bcfeatures = getbc(eduidx, edudict, tokendict, 
                               self.bcvocab, self.npref)
            for feat in bcfeatures:
                yield ('BC', 'Top2Span', feat)
        if self.firstspan is not None:
            eduidx = self.firstspan.nucedu
            bcfeatures = getbc(eduidx, edudict, tokendict,
                               self.bcvocab, self.npref)
            for feat in bcfeatures:
                yield ('BC', 'FirstSpan', feat)

