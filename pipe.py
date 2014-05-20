import os
import cPickle as pk


class Step(object):

    def __init__(self, save=None):
        self._save = save

    @property
    def save_file(self):
        return self._save

    def load(self, infile):
        return pk.load(infile)

    def xform(self, docs):
        return docs

    def save(self, docs):
        assert self._save, "Save file path should have been specified"
        with open(self._save, 'w') as outfile:
            pk.dump(docs, outfile)


class Pipe(object):

    def __init__(self, load_intermediate=False):
        self._steps = []
        self._load_intermediate = load_intermediate

    def add_step(self, step):
        self._steps.append(step)

    def run(self, infile):
        assert len(self._steps) > 0, "You can't have a preprocessing pipeline without any steps"
        docs = []
        start = 0
        if self._load_intermediate:
            for n, step in enumerate(self._steps[:-1]):
                if step.save_file and os.path.isfile(step.save_file):
                    start = n + 1
        if start:
            with open(self._steps[start - 1]) as f:
                docs = self._steps[start].load(f)
        else:
            docs = self._steps[0].load(infile)
        for step in self._steps[start:]:
            docs = step.xform(docs)
            if step.save_file:
                step.save(docs)


