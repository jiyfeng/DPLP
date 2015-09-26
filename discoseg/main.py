## main.py
## Author: Yangfeng Ji
## Date: 05-03-2015
## Time-stamp: <yangfeng 09/25/2015 15:23:03>

"""
All in one module
1, build vocab
2, build training samples
3, train a segmentation model
"""

import buildvocab, buildsample, buildmodel, buildedu

# Fixed
trainpath = "data/training/"
devpath = "data/test/"
fvocab = "data/sample/vocab.pickle.gz"
ftrain = "data/sample/train.pickle.gz"
fdev = "data/sample/dev.pickle.gz"
fmodel = "model/model.pickle.gz"
# Changable
testpath = "data/neg/"
writepath = "data/neg/"

def main():
    ## Build vocab
    thresh = 5
    # buildvocab.main(trainpath, thresh, fvocab)
    ## Build training data
    # buildsample.main(trainpath, ftrain, fvocab)
    ## Build dev data
    # buildsample.main(devpath, fdev, fvocab)
    ## Training
    # buildmodel.main(ftrain, fdev, fmodel)
    ## Segmentation
    buildedu.main(fmodel, fvocab, testpath, writepath)


if __name__ == '__main__':
    main()
