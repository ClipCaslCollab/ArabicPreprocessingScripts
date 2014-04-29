import cProfile
import os
import sys


TEXT_DIR = '/fs/clip-casl-sentiment/preprocessing/book_reviews_tok_lem'
OUT_FILE = '/fs/clip-casl-sentiment/preprocessing/out.svmlite'


def load_docs(indir):
    rval = []
    for fname in os.listdir(indir):
        tmp = {}
        tmp["score"] = fname.split("_")[0]
        try:
            with open(os.path.join(indir, fname)) as infile:
                tmp["text"] = infile.read()
            rval.append(tmp)
        except IOError:
            pass
    return rval


def gen_vocab(docs):
    rval = set([])
    for doc in docs:
        for word in doc["text"].split():
            rval.add(word)
    return rval


def gen_feature_vector(doc, vocab, present=True, count=False):
    rval = []
    doc_tokens = doc["text"].split()
    doc_vocab = set(doc_tokens)
    doc_token_counts = {}

    # generate token counts
    for tok in doc_tokens:
        doc_token_counts[tok] = doc_token_counts.get(tok, 0) + 1

    # ngram presence
    for n, tok in enumerate(vocab):
        if present and tok in doc_vocab:
            rval.append((n, 1))

    # ngram count
    for n, tok in enumerate(vocab):
        if count and tok in doc_token_counts:
            rval.append((len(vocab) + n, doc_token_counts[tok]))

    return rval


def convert_to_svmlite(label, vector):
    return " ".join([label] + ["%d:%d" % (n + 1, val) for n, val in vector])


def main(argv):
    if len(argv) < 1:
        print "Usage: prepare_for_svmlite indir"
    docs = load_docs(argv[0])
    vocab = gen_vocab(docs)
    for doc in docs:
        print convert_to_svmlite(doc["score"], gen_feature_vector(doc, vocab, present=False, count=True))


#cProfile.run('main(sys.argv[1:])')
main(sys.argv[1:])
