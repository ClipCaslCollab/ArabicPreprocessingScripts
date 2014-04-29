import cPickle as pk
import cfg
import document
import os
import random
import sys
import pipe

class ShldaInputGenerator(pipe.Step):

    def __init__(self, save=None, name="arbooks", cv=False):
        super(ShldaInputGenerator, self).__init__(save)
        self._name = name
        self._cv = cv

    def save(self, docs):
        assert self._save, "Specify a path in the constructor to save this step's output to"
        if not self._cv:
            make_shlda_input(docs, self._save, self._name)
        else:
            pass
            # TODO: refactor cv function


def save_raw_files(docs, rawdir, name):
    text = os.path.join(rawdir, "text.txt")
    with open(text, 'w') as outfile:
        for doc in docs:
            outfile.write(doc.unique_id + '\t' + doc.text + '\n')
    response = os.path.join(rawdir, "response.txt")
    with open(response, 'w') as outfile:
        for doc in docs:
            outfile.write(doc.unique_id + '\t' + doc.score + '\n')


def get_vocab_and_mapping(docs):
    vocab = set([])
    for doc in docs:
        for word in doc.text.split():
            vocab.add(word)
    sorted_list = sorted(list(vocab))
    mapping = {word: idx for idx, word in enumerate(sorted_list)}
    return sorted_list, mapping


def translate_to_shlda_fmt(docs, voc_map):
    shlda_docs = []
    for doc in docs:
        counter = {}
        for word in doc.text.split():
            counter[voc_map[word]] = counter.get(voc_map[word], 0) + 1
        shlda_docs.append(counter)
    return shlda_docs


def save_shlda_files(name, format, docs):
    sorted_list, mapping = get_vocab_and_mapping(docs)
    shlda_docs = translate_to_shlda_fmt(docs, mapping)

    dat = os.path.join(format, name + ".dat")
    with open(dat, 'w') as outfile:
        for doc in shlda_docs:
            sd = [":".join([str(tok), str(count)]) for tok, count in doc.iteritems()]
            outfile.write(' '.join([str(len(doc))] + sd) + '\n')
    docinfo = os.path.join(format, name + ".docinfo")
    with open(docinfo, 'w') as outfile:
        for doc in docs:
            outfile.write(doc.unique_id + "\t" + doc.score + "\n")
    sentdat = os.path.join(format, name + ".sent-dat")
    with open(sentdat, 'w') as outfile:
        for doc in shlda_docs:
            sd = [":".join([str(tok), str(count)]) for tok, count in doc.iteritems()]
            outfile.write(' '.join(sd) + '\n')
    sentdatraw = os.path.join(format, name + ".sent-dat.raw")
    with open(sentdatraw, 'w') as outfile:
        for doc in docs:
            outfile.write("1\n")
            outfile.write(doc.text.strip() + "\n")
    wvoc = os.path.join(format, name + ".wvoc")
    with open(wvoc, 'w') as outfile:
        for word in sorted_list:
            outfile.write(word + "\n")


def make_shlda_input(docs, outdir, name):
    outdir = os.path.join(outdir, name)
    print outdir
    rawdir = os.path.join(outdir, "raw")
    format = os.path.join(outdir, "format")
    try:
        os.makedirs(rawdir)
    except OSError:
        pass
    try:
        os.makedirs(format)
    except OSError:
        pass
    save_raw_files(docs, rawdir, name)
    save_shlda_files(name, format, docs)


def make_cv_shlda_input(inpath, outpath):
    with open(inpath) as infile:
        cv_dict = pk.load(infile)
        cv_dir = os.path.join(outpath, "arbooks", "format-cv-" + str(cv_dict["n"]) + "-" + str(cv_dict["split"]))
        try:
            os.makedirs(cv_dir)
        except OSError:
            pass
        print len(cv_dict["folds"])
        for n, fold in enumerate(cv_dict["folds"]):
            fold_name = "fold-" + str(n)
            fold_dir = os.path.join(cv_dir, fold_name)
            try:
                os.makedirs(fold_dir)
            except OSError:
                pass
            save_shlda_files(fold_name + '.tr', fold_dir, fold["train"])
            save_shlda_files(fold_name + '.te', fold_dir, fold["test"])


def main(argv):
    if len(argv) < 3:
        print "Usage: python pk_to_itm.py path/to/serialized_docs other crap"
        sys.exit(1)
    with open(argv[0]) as infile:
        docs = pk.load(infile)
    make_shlda_input(docs, argv[1], argv[2])


if __name__ == '__main__':
    main(sys.argv[1:])
