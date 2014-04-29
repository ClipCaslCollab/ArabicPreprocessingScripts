import cPickle as pk
import cfg
import document
import os
import random
import sys


def prep_cv_and_save(docs, outdir, n=10, split=0.66):
    num_train = int(len(docs) * split)
    folds = []
    for fold in range(n):
        all = [doc for doc in docs]
        train_docs = []
        for _ in range(num_train):
            idx = random.randint(0, len(all) - 1)
            train_docs.append(all[idx])
            all = all[0:idx] + all[idx + 1:]
        folds.append({
            "train": train_docs,
            "test": all
            })
    cv_dict = {
            "n": n,
            "split": split,
            "folds": folds
            }
    with open(outdir, "w") as outfile:
        pk.dump(cv_dict, outfile)


def main(argv):
    if len(argv) < 4:
        print "Usage: python xvalidate.py path/to/serialized_docs path/to/serialized_output n split"
        sys.exit(1)
    with open(argv[0]) as infile:
        docs = pk.load(infile)
    prep_cv_and_save(docs, argv[1], int(argv[2]), float(argv[3]))


if __name__ == '__main__':
    main(sys.argv[1:])
