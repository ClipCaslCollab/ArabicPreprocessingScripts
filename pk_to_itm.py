import cPickle as pk
import cfg
import document
import mallet
import os
import random
import sys
import pipe


class ItmOutputter(pipe.Step):

    def __init__(self, save=None, name="arbooks"):
        super(ItmOutputter, self).__init__(save)
        self._name = name

    def save(self, docs):
        assert self._save, "You must specify a path to Itm in the ItmOutputter constructor"
        make_itm_input(docs, self._save, self._name)


TREE_HYPERPARAMS = "DEFAULT_ 0.01\n" \
    "NL_ 0.01\n" \
    "ML_ 100\n" \
    "CL_ 0.00000000001"


def make_mlt_input(docs, path):
    with open(path, 'w') as outfile:
        for doc in docs:
            outfile.write(' '.join([doc.unique_id, doc.score, doc.text, '\n']))


def prep_itm_folders(outdir, name, docs):
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


def make_itm_input(docs, outdir, name, lang="en"):
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


def main(argv):
    if len(argv) < 3:
        print "Usage: python pk_to_itm.py path/to/serialized_docs output/dir itm-corpus-name"
        sys.exit(1)
    with open(argv[0]) as infile:
        docs = pk.load(infile)
    make_itm_input(docs, argv[1], argv[2])


if __name__ == '__main__':
    main(sys.argv[1:])
