from xml.dom import minidom

'''
Read xml output from Stanford CoreNLP and extract
1. Sentence index
2. Token index (within sentence)
3. Token
4. Lemma
5. POS
6. Dependency label
7. Dependency head
8. NER
9. Partial constituent parse
'''

class TokenElem(object):
    """ Data structure for each token
    """
    def __init__(self, idx, word, lemma, pos, nertype=None):
        self.word, self.pos = word, pos
        self.idx, self.lemma = idx, lemma
        self.deptype, self.headidx = None, None
        self.nertype = nertype
        self.partialparse = None


class SentElem(object):
    """ Data structure for each sentence
    """
    def __init__(self, idx, tokenlist):
        self.tokenlist = tokenlist
        self.idx = idx


class DepElem(object):
    """ Data structure for reading dependency parsing
    """
    def __init__(self, deptype, gidx, gtoken, didx, dtoken):
        self.deptype = deptype
        self.gidx, self.gtoken = gidx, gtoken
        self.didx, self.dtoken = didx, dtoken
        

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


def getTokens(sent):
    tokens = sent.getElementsByTagName('token')
    tokenelem_dict = {}
    for token in tokens:
        pos = getText(token.getElementsByTagName('POS')[0].childNodes)
        pos = pos.encode("ascii","ignore")
        word = getText(token.getElementsByTagName('word')[0].childNodes)
        word = word.encode("ascii","ignore")
        lemma = getText(token.getElementsByTagName('lemma')[0].childNodes)
        lemma = lemma.encode("ascii","ignore")
        try:
            ner = getText(token.getElementsByTagName('NER')[0].childNodes)
            ner = ner.encode("ascii","ignore")
        except IndexError:
            ner = None
        idx = int(token.attributes['id'].value)
        token = TokenElem(idx, word, lemma, pos, ner)
        tokenelem_dict[idx] = token
    return tokenelem_dict


def getConstituenttree(sent):
    tree = sent.getElementsByTagName('parse')
    tree = getText(tree[0].childNodes)
    return tree


def getDeptree(sent):
    deps_group = sent.getElementsByTagName('dependencies')
    for item in deps_group:
        if item.attributes['type'].value == 'basic-dependencies':
            deps = item.getElementsByTagName('dep')
        else:
            # print item.attributes['type'].value
            pass
    depelem_list = []
    for dep in deps:
        deptype = dep.attributes['type'].value
        governor = dep.getElementsByTagName('governor')
        gidx = int(governor[0].attributes['idx'].value)
        gtoken = getText(governor[0].childNodes)
        dependent = dep.getElementsByTagName('dependent')
        didx = int(dependent[0].attributes['idx'].value)
        dtoken = getText(dependent[0].childNodes)
        elem = DepElem(deptype, gidx, gtoken, didx, dtoken)
        depelem_list.append(elem)
    return depelem_list


def integrate(token_dict, dep_list):
    """ Integrate dependency information into token list
    """
    for dep in dep_list:
        deptype = dep.deptype
        gidx, gtoken = dep.gidx, dep.gtoken
        didx, dtoken = dep.didx, dep.dtoken
        tokenelem = token_dict[didx]
        tokenelem.deptype = deptype
        tokenelem.headidx = gidx
        token_dict[didx] = tokenelem
    token_list = []
    for idx in range(len(token_dict)):
        token_list.append(token_dict[idx+1])
    return token_list
    

def reader(fname):
    xmldoc = minidom.parse(fname)
    sentelem_list = []
    constituent_list = []
    sentlist = xmldoc.getElementsByTagName('sentences')[0].getElementsByTagName('sentence')
    for (idx, sent) in enumerate(sentlist):
        tokenelem_dict = getTokens(sent)
        tree = getConstituenttree(sent)
        constituent_list.append(tree)
        depelem_list = getDeptree(sent)
        tokenelem_list = integrate(tokenelem_dict, depelem_list)
        sentelem_list.append(SentElem(idx, tokenelem_list))
    return sentelem_list, constituent_list


def combineparse2sent(sent, parse):
    """ Combine constitent parse into sent
    """
    parse = parse.split()
    tokenlist = [token.word for token in sent.tokenlist]
    parselist, tidx = [""]*len(tokenlist), 0
    while parse:
        item = parse.pop(0)
        parselist[tidx] += (" " + item)
        partialparse = parselist[tidx].replace(' ','')
        partialparse = partialparse.encode("ascii", "ignore")
        word = tokenlist[tidx].replace(' ','')
        # print word, partialparse
        if (word + ')') in partialparse:
            tidx += 1
    # Attach to sent
    for (tidx, token) in enumerate(sent.tokenlist):
        item = parselist[tidx]
        item = item.encode("ascii", "ignore")
        sent.tokenlist[tidx].partialparse = item
    return sent


def combine(sentlist, constlist):
    """
    """
    for (sidx, sent) in enumerate(sentlist):
        parse = constlist[sidx]
        sent = combineparse2sent(sent, parse)
        sentlist[sidx] = sent
    return sentlist

        
def writer(sentlist, fconll):
    with open(fconll, 'w') as fout:
        for sent in sentlist:
            for token in sent.tokenlist:
                line = str(sent.idx) + '\t' + str(token.idx) + '\t' + token.word + '\t' + token.lemma + '\t' + str(token.pos) + '\t' + str(token.deptype) + '\t' + str(token.headidx) + '\t' + str(token.nertype) + '\t' + str(token.partialparse) + '\n'
                line = line.encode('ascii', 'ignore')
                fout.write(line)
            fout.write('\n')


if __name__ == '__main__':
    sentlist, constlist = reader('test.xml')
    sentlist = combine(sentlist, constlist)
    writer(sentlist, 'test.conll')
        
