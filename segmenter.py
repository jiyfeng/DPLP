""" Call a pretrained segmenter for discourse segmentation
"""

import discoseg.buildedu as buildedu
from sys import argv

def main(readpath, writepath):
    fmodel = "discoseg/pretrained/model.pickle.gz"
    fvocab = "discoseg/pretrained/vocab.pickle.gz"
    buildedu.main(fmodel, fvocab, readpath, writepath)

if __name__ == '__main__':
    if len(argv) == 2:
        readpath = argv[1]
        writepath = argv[1]
        main(readpath, writepath)
    elif len(argv) == 3:
        readpath = argv[1]
        writepath = argv[2]
        main(readpath, writepath)
    else:
        print "python segmenter.py read_path [write_path]"
        print "\tread_path - the document folder"
