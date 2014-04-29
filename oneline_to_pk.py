import codecs
import cPickle as pk
import cfg
import document
import re
import sys
import pipe


class OneDocPerLine(pipe.Step):

    def load(self, infile):
        rval = []
        for line in infile:
            fields = line.split()
            tmp = document.Document(' '.join(fields[2:]),
                                fields[1],
                                uid=fields[0])
            rval.append(tmp)
        return rval


def load_corpus(corpus_path):
    rval = []
    with open(corpus_path, 'r') as infile:
        for line in infile:
            fields = line.split()
            tmp = document.Document(' '.join(fields[2:]),
                                fields[1],
                                uid=fields[0])
            rval.append(tmp)
    return rval


def load_and_serialize(corpus_path, pk_path):
    docs = load_corpus(corpus_path)
    with open(pk_path, 'w') as outfile:
        pk.dump(docs, outfile)


def main(argv):
    if len(argv) < 2:
        print "Usage: python oneline_to_pk.py path/to/oneline_per_file__corpus path/to/serialized_output"
        sys.exit(1)
    odl = OneDocPerLine(save=argv[1])
    with open(argv[0]) as infile:
        docs = odl.load(infile)
        docs = odl.xform(docs)
        odl.save(docs)


if __name__ == '__main__':
    main(sys.argv[1:])
