## buildtree.py
## Author: Yangfeng Ji
## Date: 09-10-2014
## Time-stamp: <yangfeng 09/25/2015 16:44:42>

from datastructure import *
from util import extractrelation

def BFT(tree):
    """ Breadth-first treavsal on general RST tree

    :type tree: SpanNode instance
    :param tree: an general RST tree
    """
    queue = [tree]
    bft_nodelist = []
    while queue:
        node = queue.pop(0)
        bft_nodelist.append(node)
        queue += node.nodelist
    return bft_nodelist


def BFTbin(tree):
    """ Breadth-first treavsal on binary RST tree

    :type tree: SpanNode instance
    :param tree: an binary RST tree
    """
    queue = [tree]
    bft_nodelist = []
    while queue:
        node = queue.pop(0)
        bft_nodelist.append(node)
        if node.lnode is not None:
            queue.append(node.lnode)
        if node.rnode is not None:
            queue.append(node.rnode)
    return bft_nodelist


def postorder_DFT(tree, nodelist):
    """ Post order traversal on binary RST tree

    :type tree: SpanNode instance
    :param tree: an binary RST tree

    :type nodelist: list
    :param nodelist: list of node in post order
    """
    if tree.lnode is not None:
        postorder_DFT(tree.lnode, nodelist)
    if tree.rnode is not None:
        postorder_DFT(tree.rnode, nodelist)
    nodelist.append(tree)
    return nodelist


def getparse(tree, parse):
    """ Get parse tree

    :type tree: SpanNode instance
    :param tree: an binary RST tree

    :type parse: string
    :param parse: parse tree in string format
    """
    if (tree.lnode is None) and (tree.rnode is None):
        # Leaf node
        parse += " ( EDU " + str(tree.nucedu)
    else:
        parse += " ( " + tree.form
        # get the relation from its satellite node
        if tree.form == 'NN':
            parse += "-" + extractrelation(tree.rnode.relation)
        elif tree.form == 'NS':
            parse += "-" + extractrelation(tree.rnode.relation)
        elif tree.form == 'SN':
            parse += "-" + extractrelation(tree.lnode.relation)
        else:
            raise ValueError("Unrecognized N-S form")
    # print tree.relation
    if tree.lnode is not None:
        parse = getparse(tree.lnode, parse)
    if tree.rnode is not None:
        parse = getparse(tree.rnode, parse)
    parse += " ) "
    return parse
        

def checkcontent(label, c):
    """ Check whether the content is legal

    :type label: string
    :param label: parsing label, such 'span', 'leaf'

    :type c: list
    :param c: list of tokens
    """
    if len(c) > 0:
        raise ValueError("{} with content={}".format(label, c))


def createtext(lst):
    """ Create text from a list of tokens

    :type lst: list
    :param lst: list of tokens
    """
    newlst = []
    for item in lst:
        item = item.replace("_!","")
        newlst.append(item)
    text = ' '.join(newlst)
    # Lower-casing
    return text.lower()


def processtext(tokens):
    """ Preprocessing token list for filtering '(' and ')' in text

    :type tokens: list
    :param tokens: list of tokens
    """
    identifier = '_!'
    within_text = False
    for (idx, tok) in enumerate(tokens):
        if identifier in tok:
            for _ in range(tok.count(identifier)):
                within_text = not within_text
        if ('(' in tok) and (within_text):
            tok = tok.replace('(','-LB-')
        if (')' in tok) and (within_text):
            tok = tok.replace(')','-RB-')
        tokens[idx] = tok
    return tokens
    

def createnode(node, content):
    """ Assign value to an SpanNode instance

    :type node: SpanNode instance
    :param node: A new node in an RST tree

    :type content: list
    :param content: content from stack
    """
    for c in content:
        if isinstance(c, SpanNode):
            # Sub-node
            node.nodelist.append(c)
            c.pnode = node
        elif c[0] == 'span':
            node.eduspan = (c[1], c[2])
        elif c[0] == 'relation':
            node.relation = c[1]
        elif c[0] == 'leaf':
            node.eduspan = (c[1], c[1])
            node.nucspan = (c[1], c[1])
            node.nucedu = c[1]
        elif c[0] == 'text':
            node.text = c[1]
        else:
            raise ValueError("Unrecognized property: {}".format(c[0]))
    return node


def buildtree(text):
    """ Build tree from *.dis file

    :type text: string
    :param text: RST tree read from a *.dis file
    """
    tokens = text.strip().replace('//TT_ERR','').replace('\n','').replace('(', ' ( ').replace(')', ' ) ').split()
    # print 'tokens = {}'.format(tokens)
    queue = processtext(tokens)
    # print 'queue = {}'.format(queue)
    stack = []
    while queue:
        token = queue.pop(0)
        if token == ')':
            # If ')', start processing
            content = [] # Content in the stack
            while stack:
                cont = stack.pop()
                if cont == '(':
                    break
                else:
                    content.append(cont)
            content.reverse() # Reverse to the original order
            # Parse according to the first content word
            if len(content) < 2:
                raise ValueError("content = {}".format(content))
            label = content.pop(0)
            if label == 'Root':
                node = SpanNode(prop=label)
                node = createnode(node, content)
                stack.append(node)
            elif label == 'Nucleus':
                node = SpanNode(prop=label)
                node = createnode(node, content)
                stack.append(node)
            elif label == 'Satellite':
                node = SpanNode(prop=label)
                node = createnode(node, content)
                stack.append(node)
            elif label == 'span':
                # Merge
                beginindex = int(content.pop(0))
                endindex = int(content.pop(0))
                stack.append(('span', beginindex, endindex))
            elif label == 'leaf':
                # Merge 
                eduindex = int(content.pop(0))
                checkcontent(label, content)
                stack.append(('leaf', eduindex, eduindex))
            elif label == 'rel2par':
                # Merge
                relation = content.pop(0)
                checkcontent(label, content)
                stack.append(('relation',relation))
            elif label == 'text':
                # Merge
                txt = createtext(content)
                stack.append(('text', txt))
            else:
                raise ValueError("Unrecognized parsing label: {} \n\twith content = {}\n\tstack={}\n\tqueue={}".format(label, content, stack, queue))
        else:
            # else, keep push into the stack
            stack.append(token)
    return stack[-1]
        

def binarizetree(tree):
    """ Convert a general RST tree to a binary RST tree

    :type tree: instance of SpanNode
    :param tree: a general RST tree
    """
    queue = [tree]
    while queue:
        node = queue.pop(0)
        queue += node.nodelist
        # Construct binary tree
        if len(node.nodelist) == 2:
            node.lnode = node.nodelist[0]
            node.rnode = node.nodelist[1]
            # Parent node
            node.lnode.pnode = node
            node.rnode.pnode = node
        elif len(node.nodelist) > 2:
            # Remove one node from the nodelist
            node.lnode = node.nodelist.pop(0)
            newnode = SpanNode(node.nodelist[0].prop)
            newnode.nodelist += node.nodelist
            # Right-branching
            node.rnode = newnode
            # Parent node
            node.lnode.pnode = node
            node.rnode.pnode = node
            # Add to the head of the queue
            # So the code will keep branching
            # until the nodelist size is 2
            queue.insert(0, newnode)
        # Clear nodelist for the current node
        node.nodelist = []
    return tree


def backprop(tree, doc):
    """ Starting from leaf node, propagating node
        information back to root node

    :type tree: SpanNode instance
    :param tree: an binary RST tree
    """
    treenodes = BFTbin(tree)
    treenodes.reverse()
    for node in treenodes:
        if (node.lnode is not None) and (node.rnode is not None):
            # Non-leaf node
            node.eduspan = __getspaninfo(node.lnode, node.rnode)
            node.text = __gettextinfo(doc.edudict, node.eduspan)
            if node.relation is None:
                # If it is a new node created by binarization
                if node.prop == 'Root':
                    pass
                else:
                    node.relation = __getrelationinfo(node.lnode,
                        node.rnode)
            node.form, node.nucspan = __getforminfo(node.lnode,
                node.rnode)
        elif (node.lnode is None) and (node.rnode is not None):
            raise ValueError("Unexpected left node")
        elif (node.lnode is not None) and (node.rnode is None):
            raise ValueError("Unexpected right node")
        else:
            # Leaf node
            node.text = __gettextinfo(doc.edudict, node.eduspan)
    return treenodes[-1]


def __getspaninfo(lnode, rnode):
    """ Get span size for parent node

    :type lnode,rnode: SpanNode instance
    :param lnode,rnode: Left/Right children nodes
    """
    try:
        eduspan = (lnode.eduspan[0], rnode.eduspan[1])
    except TypeError:
        print lnode.prop, rnode.prop
        print lnode.nucspan, rnode.nucspan
    return eduspan


def __getforminfo(lnode, rnode):
    """ Get Nucleus/Satellite form and Nucleus span

    :type lnode,rnode: SpanNode instance
    :param lnode,rnode: Left/Right children nodes
    """
    if (lnode.prop=='Nucleus') and (rnode.prop=='Satellite'):
        nucspan = lnode.eduspan
        form = 'NS'
    elif (lnode.prop=='Satellite') and (rnode.prop=='Nucleus'):
        nucspan = rnode.eduspan
        form = 'SN'
    elif (lnode.prop=='Nucleus') and (rnode.prop=='Nucleus'):
        nucspan = (lnode.eduspan[0], rnode.eduspan[1])
        form = 'NN'
    else:
        raise ValueError("")
    return (form, nucspan)


def __getrelationinfo(lnode, rnode):
    """ Get relation information

    :type lnode,rnode: SpanNode instance
    :param lnode,rnode: Left/Right children nodes
    """
    if (lnode.prop=='Nucleus') and (rnode.prop=='Nucleus'):
        relation = lnode.relation
    elif (lnode.prop=='Nucleus') and (rnode.prop=='Satellite'):
        relation = lnode.relation
    elif (lnode.prop=='Satellite') and (rnode.prop=='Nucleus'):
        relation = rnode.relation
    else:
        print 'lnode.prop = {}, lnode.eduspan = {}'.format(lnode.prop, lnode.eduspan)
        print 'rnode.prop = {}, lnode.eduspan = {}'.format(rnode.prop, rnode.eduspan)
        raise ValueError("Error when find relation for new node")
    return relation


def __gettextinfo(edudict, eduspan):
    """ Get text span for parent node

    :type edudict: dict of list
    :param edudict: EDU from this document

    :type eduspan: tuple with two elements
    :param eduspan: start/end of EDU IN this span
    """
    # text = lnode.text + " " + rnode.text
    text = []
    for idx in range(eduspan[0], eduspan[1]+1, 1):
        text += edudict[idx]
    # Return: A list of token indices
    return text


def decodeSRaction(tree):
    """ Decoding Shift-reduce actions from an binary RST tree

    :type tree: SpanNode instance
    :param tree: an binary RST tree
    """
    # Start decoding
    post_nodelist = postorder_DFT(tree, [])
    # print len(post_nodelist)
    actionlist = []
    for node in post_nodelist:
        if (node.lnode is None) and (node.rnode is None):
            actionlist.append(('Shift', None, None))
        elif (node.lnode is not None) and (node.rnode is not None):
            form = node.form
            if (form == 'NN') or (form == 'NS'):
                relation = extractrelation(node.rnode.relation)
            else:
                relation = extractrelation(node.lnode.relation)
            actionlist.append(('Reduce', form, relation))
        else:
            raise ValueError("Can not decode Shift-Reduce action")
    return actionlist


def getedunode(tree):
    """ Get all left nodes. It can be used for generating training
        examples from gold RST tree

    :type tree: SpanNode instance
    :param tree: an binary RST tree
    """
    # Post-order depth-first traversal
    post_nodelist = postorder_DFT(tree, [])
    # EDU list
    edulist = []
    for node in post_nodelist:
        if (node.lnode is None) and (node.rnode is None):
            edulist.append(node)
    return edulist
        
        
## ========================================================
def test():
    fname = "examples/wsj_0604.out.dis"
    text = open(fname, 'r').read()
    # Build RST tree
    T = buildtree(text)
    bft_nodelist = BFT(T)
    # print len(bft_nodelist)
    # Binarize the RST tree
    T = binarizetree(T)
    # Back-propagating information from
    #   leaf node to root node
    T = backprop(T)
    # Decoding shift-reduce actions from
    #   the binary RST tree
    actionlist = decodeSRaction(T)
    # for action in actionlist:
    #     print action


if __name__ == '__main__':
    test()
