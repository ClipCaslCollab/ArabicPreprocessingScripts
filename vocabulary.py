import document
import sys
import cPickle


def get_voc(docs):
    return {word for doc in docs for word in doc.text.split()}


def voc_size(docs):
    return len(get_voc(docs))


def longest_word(docs):
    return max(get_voc(docs), key=lambda word: len(word))


def shortest_word(docs):
    return min(get_voc(docs), key=lambda word: len(word))


def ave_word_len(docs):
    word_size_sum = sum(len(word) for doc in docs for word in doc.text.split())
    num_words = len([word for doc in docs for word in doc.text.split()])
    return word_size_sum / num_words


def ave_unique_word_len(docs):
    vocab = get_voc(docs)
    return sum(len(word) for word in vocab) / voc_size(docs)


def num_toks(docs):
    return len([word for doc in docs for word in doc.text.split()])


def main(argv):
    with open(argv[0]) as f:
        docs = cPickle.load(f)
        print voc_size(docs)
        print longest_word(docs)
        print shortest_word(docs)
        print ave_word_len(docs)
        print ave_unique_word_len(docs)
        print num_toks(docs)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
