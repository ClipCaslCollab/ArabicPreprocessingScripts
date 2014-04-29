import document
import sys
import cPickle as pk


def count_voc(docs):
    voc = set([])
    for doc in docs:
        for word in doc.text.split():
            voc.add(word)
    return len(voc)


def main(argv):
    with open(argv[0]) as f:
        print count_voc(pk.load(f))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
