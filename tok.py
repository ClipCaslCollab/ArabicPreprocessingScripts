import cPickle as pk
import cfg
import document
from itertools import izip
import os
import sys
from nltk.tokenize import word_tokenize
from nltk.stem.porter import *
from nltk.corpus import stopwords
import pipe


class Tokenizer(pipe.Step):

    def __init__(self, save=None, lang="en", stem=True, remove_stopwords=True):
        super(Tokenizer, self).__init__(save)
        self._lang = lang
        self._stem = stem
        self._rmsw = remove_stopwords

    def xform(self, docs):
        if self._lang == "en":
            stemmer = PorterStemmer()
            stp = set(stopwords.words("english"))
            # TODO: maybe shouldn't modify the objects that get passed in, but it shouldn't matter
            for doc in docs:
                tok = word_tokenize(doc.text.lower())
                if self._stem:
                    tok = [stemmer.stem(w) for w in tok if not self._rmsw or w not in stp]
                doc.text = " ".join(tok)
            return docs
        elif self._lang == "ar":
            if not self._stem:
                flat_file_path = os.path.join(cfg.SCRATCH_PATH, str(os.getpid()) + "docs.flat")
                create_flat_file(docs, flat_file_path)
                tokenize_ar(flat_file_path)
                replace_text(docs, flat_file_path + ".ATB.tok", self._stem)
            else:
                for doc in docs:
                    flat_file_path = os.path.join(cfg.SCRATCH_PATH, str(os.getpid()) + "docs.flat")
                    with open(flat_file_path, "w") as outfile:
                        write_doc_to_file(doc, outfile)
                    tokenize_ar(flat_file_path)
                    with open(flat_file_path + ".mada") as infile:
                        text = infile.read()
                        print text
                        toks = re.findall(r'stem:([^\s]*)', text)
                        print " ".join(toks)
                        doc.text = " ".join(toks)
            return docs


def write_doc_to_file(doc, outfile):
    #outfile.write(doc.text.encode("utf-8"))
    outfile.write(doc.text)
    outfile.write("\n")


def create_flat_file(docs, flat_file_path):
    with open(flat_file_path, "w") as outfile:
        for doc in docs:
            write_doc_to_file(doc, outfile)


def tokenize_ar(flat_file_path):
    cmd = "java -Xmx2500m -Xms2500m -XX:NewRatio=3 -jar %s -rawinput %s -rawoutdir %s -rawconfig %s"
    jar = os.path.join(cfg.MADA_PATH, cfg.MADA_JAR)
    config = os.path.join(cfg.MADA_PATH, cfg.MADA_CFG)
    print cmd % (jar, flat_file_path, cfg.SCRATCH_PATH, config)
    os.system(cmd % (jar, flat_file_path, cfg.SCRATCH_PATH, config))


def replace_text(docs, tok_file_path, stem):
    with open(tok_file_path + ".ATB.tok") as infile:
        for doc, text in izip(docs, infile):
            doc.text = text


def tokenize_and_replace(docs, outpath, lang):
    if lang == "ar":
        tok = Tokenizer(save=outpath, lang=lang)
        docs = tok.xform(docs)
        tok.save(docs)
        #flat_file_path = os.path.join(cfg.SCRATCH_PATH, "docs.flat")
        #create_flat_file(docs, flat_file_path)
        #tokenize_ar(flat_file_path)
        #replace_text(docs, flat_file_path + ".ATB.tok")
        #with open(outpath, "w") as outfile:
        #    pk.dump(docs, outfile)
    elif lang == "en":
        stemmer = PorterStemmer()
        stp = set(stopwords.words("english"))
        for doc in docs:
            tok = word_tokenize(doc.text.lower())
            stm = [stemmer.stem(w) for w in tok if w not in stp]
            doc.text = " ".join(stm)
        with open(outpath, "w") as outfile:
            pk.dump(docs, outfile)


def main(argv):
    if len(argv) < 2:
        print "Usage: python xml_to_pk.py path/to/serialized_docs path/to/serialized_output"
        sys.exit(1)
    tk = Tokenizer(save=argv[1]);
    with open(argv[0]) as infile:
        docs = tk.load(infile)
        docs = tk.xform(docs)
        tk.save(docs)
    #tokenize_and_replace(docs, argv[1])


if __name__ == '__main__':
    main(sys.argv[1:])
