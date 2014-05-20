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

