import cPickle as pk
import cfg
import document
import os
import sys
import pipe


class RareWordRemover(pipe.Step):

    def __init__(self, save=None, thresh=2):
        super(RareWordRemover, self).__init__(save)
        self._thresh = thresh

    def xform(self, docs):
        counts = doc_counts_by_word(docs)
        for doc in docs:
            tmp = [w for w in doc.text.split() if counts[w] > self._thresh]
            doc.text = " ".join(tmp)
        return docs


def doc_counts_by_word(docs):
    counts = {}
    for doc in docs:
        doc_voc = set([w for w in doc.text.split()])
        for w in doc_voc:
            counts[w] = counts.get(w, 0) + 1
    return counts


def remove_rare_words_and_save(docs, outpath, thresh=2):
    counts = doc_counts_by_word(docs)
    for doc in docs:
        tmp = [w for w in doc.text.split() if counts[w] > thresh]
        doc.text = " ".join(tmp)
    with open(outpath, "w") as outfile:
        pk.dump(docs, outfile)


def main(argv):
    if len(argv) < 2:
        print "Usage: python xml_to_pk.py path/to/serialized_docs path/to/serialized_output"
        sys.exit(1)
    with open(argv[0]) as infile:
        docs = pk.load(infile)
    remove_rare_words_and_save(docs, argv[1])


if __name__ == '__main__':
    main(sys.argv[1:])
