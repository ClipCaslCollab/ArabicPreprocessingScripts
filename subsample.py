import cPickle as pk
import cfg
import document
import random
import sys
import pipe


class Subsampler(pipe.Step):

    def __init__(self, save=None, n=1000, rand=True, ratios=None):
        super(Subsampler, self).__init__(save)
        self._n = n
        self._rand = rand
        self._ratios = ratios

    def xform(self, docs):
        rval = []
        labels = set([doc.score for doc in docs])
        docs_by_label = {label: [doc for doc in docs if doc.score == label] for label in labels}
        docs_by_label_backup = {label: [doc for doc in docs if doc.score == label] for label in labels}
        if not self._ratios:
            self._ratios = {label: 1 for label in labels}
        assert len(self._ratios) == len(labels), "You must supply the same number of ratios as there are labels"
        if self._rand:
            for label, lst in docs_by_label.iteritems():
                random.shuffle(lst)
        #n = min(n, *[len(lst) * len(labels) for label, lst in docs_.iteritems()])
        while len(rval) < self._n:
            for label in labels:
                for _ in range(self._ratios[label]):
                    if docs_by_label[label]:
                        rval.append(docs_by_label[label][0])
                        docs_by_label[label] = docs_by_label[label][1:]
                    else:
                        rval.append(random.choice(docs_by_label_backup[label]))
        return rval


def subsample(docs, n, rand=True, ratios=None):
    rval = []
    labels = set([doc.score for doc in docs])
    docs_by_label = {label: [doc for doc in docs if doc.score == label] for label in labels}
    docs_by_label_backup = {label: [doc for doc in docs if doc.score == label] for label in labels}
    if not ratios:
        ratios = {label: 1 for label in labels}
    assert len(ratios) == len(labels), "You must supply the same number of ratios as there are labels"
    if rand:
        for label, lst in docs_by_label.iteritems():
            random.shuffle(lst)
    #n = min(n, *[len(lst) * len(labels) for label, lst in docs_.iteritems()])
    while len(rval) < n:
        for label in labels:
            for _ in range(ratios[label]):
                if docs_by_label[label]:
                    rval.append(docs_by_label[label][0])
                    docs_by_label[label] = docs_by_label[label][1:]
                else:
                    rval.append(random.choice(docs_by_label_backup[label]))
    return rval


def subsample_and_save(outpath, docs, n, rand=True, ratios=None):
    ssdocs = subsample(docs, n, rand=rand, ratios=ratios)
    with open(outpath, "w") as outfile:
        pk.dump(ssdocs, outfile)


def main(argv):
    if len(argv) < 3:
        print "Usage: python subsample.py path/to/serialized_docs path/to/serialized_output n"
        sys.exit(1)
    sub = Subsampler(save=argv[1], n=int(argv[2]))
    with open(argv[0]) as infile:
        docs = sub.load(infile)
        docs = sub.xform(docs)
        sub.save(docs)
    #subsample_and_save(argv[1], docs, int(argv[2]))


if __name__ == '__main__':
    main(sys.argv[1:])
