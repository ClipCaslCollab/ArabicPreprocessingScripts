"""
gen_features.py

Takes a list of pickled documents and a doc-topics output file from mallet as input.
Outputs features for each document in svmlite format.
Default features are word counts and topic proportions.
"""
import argparse
import cPickle as pk
from itertools import izip
import sys
import document
import vocabulary


def doc_feats(voc, doc, top_props, count_feats, binary_feats, topic_feats):
    feature_vec = []
    word_counts = {}

    for word in doc.text.split():
        word_counts[word] = word_counts.get(word, 0) + 1

    if count_feats:
        for word in list(voc):
            feature_vec.append(word_counts.get(word, 0))
    
    if binary_feats:
        for word in list(voc):
            if word in word_counts:
                feature_vec.append(1)
            else:
                feature_vec.append(0)

    if topic_feats:
        for top, prop in top_props.iteritems():
            feature_vec.append(prop)

    return feature_vec


def doc_feats_to_string(doc_id, feat_vec):
    return str(doc_id) + " " + " ".join(str(n) + ":" + str(val) for n, val in enumerate(feat_vec))


def corpus_features(docs, doc_topics, count_feats=True, binary_feats=True, topic_feats=True):
    assert len(docs) == len(doc_topics), "The number of documents in the corpus and doc topics files should be the same"
    cfeats = []
    voc = vocabulary.get_voc(docs)
    for doc, top_props in zip(docs, doc_topics):
        dfeats = doc_feats(voc, doc, top_props, count_feats, binary_feats, topic_feats)
        cfeats.append(dfeats)
    return cfeats


def corpus_features_to_string(docs, cfeats):
    docfeat_strings = []
    for doc, feat_vec in zip(docs, cfeats):
        docfeat_strings.append(doc_feats_to_string(doc.unique_id, feat_vec))
    return "\n".join(docfeat_strings)


def group(l, n=2):
    itr = iter(l)
    return izip(*([itr] * n))


def doc_topics_from_file(doc_topic_file):
    doc_topics = []
    lines = doc_topic_file.readlines()[1:]
    for line in lines:
        top_props = {topic: prop for topic, prop in group(line.split()[2:])}
        doc_topics.append(top_props)
    return doc_topics


def main(argv):
    parser = argparse.ArgumentParser(description="svmlite fature generator")
    parser.add_argument("-b", dest="binary_feats", action="store_true", help="Generate word presence features")
    parser.add_argument("-no-c", dest="count_feats", action="store_false", help="Don't generate word count features")
    parser.add_argument("-no-t", dest="topic_feats", action="store_false", help="Don't generate topic proportion features")
    parser.add_argument("-dt", dest="doc_topics", help="Mallet doc topics file")
    parser.add_argument("docs", help="Pickled documents")
    arguments = parser.parse_args(argv)
    docs = []
    with open(arguments.docs) as f:
        docs = pk.load(f)
    assert docs, "There were problems loading the documents"
    doc_topics = []
    if arguments.topic_feats and arguments.doc_topics:
        with open(arguments.doc_topics) as f:
            doc_topics = doc_topics_from_file(f)
    elif not arguments.topic_feats:
        doc_topics = [{} for _ in docs]
    assert doc_topics, "There were problems loading the doc topics"
    cfeats = corpus_features(docs, doc_topics, count_feats=arguments.count_feats,
            binary_feats=arguments.binary_feats, topic_feats=arguments.topic_feats)
    print corpus_features_to_string(docs, cfeats)


if __name__ == '__main__':
    main(sys.argv[1:])
