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
import string


class Tokenizer(pipe.Step):

    def __init__(self, save=None, lang="en", stem=True, remove_stopwords=True):
        super(Tokenizer, self).__init__(save)
        self._lang = lang
        self._stem = stem
        self._rmsw = remove_stopwords

    def xform(self, docs):
        if self._lang == "en":
            return self.tok_en(docs)
        elif self._lang == "ar":
            return self.tok_ar(docs)

    def tok_en(self, docs):
        stemmer = PorterStemmer()
        stp = set(stopwords.words("english")).union(set(string.punctuation))
        for doc in docs:
            tok = word_tokenize(doc.text.lower())
            if self._stem:
                tok = [w for w in tok if not self._rmsw or w not in stp]
                tok = [stemmer.stem(w) for w in tok]
            doc.text = " ".join(tok)
        return docs

    def tok_ar(self, docs):
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

