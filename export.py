import cPickle as pk
import cfg
import document
import mallet
import os
import random
import sys
import pipe

class ShldaExporter(pipe.Step):

    def __init__(self, save=None, name="arbooks", cv=False):
        super(ShldaExporter, self).__init__(save)
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
    with open(text, 'wb') as outfile:
        for doc in docs:
            outfile.write((doc.unique_id + '\t' + doc.text + '\n').encode('utf-8'))
    response = os.path.join(rawdir, "response.txt")
    with open(response, 'wb') as outfile:
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
    with open(dat, 'wb') as outfile:
        for doc in shlda_docs:
            sd = [":".join([str(tok), str(count)]) for tok, count in doc.iteritems()]
            outfile.write(' '.join([str(len(doc))] + sd) + '\n')
    docinfo = os.path.join(format, name + ".docinfo")
    with open(docinfo, 'wb') as outfile:
        for doc in docs:
            outfile.write(doc.unique_id + "\t" + doc.score + "\n")
    sentdat = os.path.join(format, name + ".sent-dat")
    with open(sentdat, 'wb') as outfile:
        for doc in shlda_docs:
            sd = [":".join([str(tok), str(count)]) for tok, count in doc.iteritems()]
            outfile.write(' '.join(sd) + '\n')
    sentdatraw = os.path.join(format, name + ".sent-dat.raw")
    with open(sentdatraw, 'wb') as outfile:
        for doc in docs:
            outfile.write("1\n")
            outfile.write((doc.text.strip() + "\n").encode('utf-8'))
    wvoc = os.path.join(format, name + ".wvoc")
    with open(wvoc, 'w') as outfile:
        for word in sorted_list:
            outfile.write((word + "\n").encode('utf-8'))


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


class ItmExporter(pipe.Step):

    def __init__(self, save=None, name="arbooks", lang="ar"):
        super(ItmExporter, self).__init__(save)
        self._name = name
        self._lang = lang

    def save(self, docs):
        assert self._save, "You must specify a path to Itm in the ItmOutputter constructor"
        make_itm_input(docs, self._save, self._name, lang=self._lang)


TREE_HYPERPARAMS = "DEFAULT_ 0.01\n" \
    "NL_ 0.01\n" \
    "ML_ 100\n" \
    "CL_ 0.00000000001"


def make_mlt_input(docs, path):
    with open(path, 'w') as outfile:
        for doc in docs:
            outfile.write(' '.join([doc.unique_id, doc.score, doc.text, '\n']))


def prep_itm_folders(outdir, name, docs):
    datapath = os.path.join(outdir, 'data')
    if not os.path.isdir(datapath):
        os.makedirs(datapath)
    try:
        inpath = os.path.join(outdir, 'results/' + name + '/input')
        outpath = os.path.join(outdir, 'results/' + name + '/output')
        os.makedirs(inpath)
        os.makedirs(outpath)
    except OSError:
        os.system("rm -rf " + os.path.join(outdir, 'results/' + name + '/input', name + '.voc'))
        os.system("rm -rf " + os.path.join(outdir, 'results/' + name + '/output/*'))
    with open(os.path.join(inpath, name + ".url"), "w") as outfile:
        for doc in docs:
            outfile.write(" ".join([doc.unique_id, "data/" + name + "#" + doc.unique_id]))
            outfile.write("\n")
    with open(os.path.join(inpath, "tree_hyperparams"), "w") as outfile:
        outfile.write(TREE_HYPERPARAMS)


def make_itm_input(docs, outdir, name, lang):
    prep_itm_folders(outdir, name, docs)
    flat_file = os.path.join(cfg.SCRATCH_PATH, "docs.flat")
    make_mlt_input(docs, flat_file)
    mlt = mallet.Mallet(cfg.MALLET_BIN_PATH)
    mltout = os.path.join(outdir, 'results/' + name + '/input', name + '-topic-input.mallet')
    mlt.import_file(flat_file, mltout, lang)
    doc_div_tmpl = "<div class=\"segment\" id=\"%s\"> <p> %s </p> </div>"
    html_path = os.path.join(outdir, 'data/', name + '.html')
    with open(cfg.ITM_HTML_TEMPLATE_PATH) as html_template:
        html = html_template.read()
        with open(html_path, 'w') as outfile:
            outfile.write(html.encode('utf-8'))
            outfile.write('\n'.join(doc_div_tmpl % (doc.unique_id, doc.text) for doc in docs))
            outfile.write('</div>\n</body>\n</html>')

