import codecs
import cPickle as pk
import cfg
import document
import re
import sys
import xml.etree.ElementTree as ET


BAD_XML = r'<SOURCELINK>.*</SOURCELINK>'


def load_corpus(corpus_path):
    rval = []
    with open(corpus_path, 'r') as infile:
        text = '\n'.join(re.sub(BAD_XML, '', line) for line in infile)
        documents = ET.fromstring(text)
        for document in documents:
            tmp = {}
            tmp = document.Document(document.find('TEXT').text,
                                    document.find('SCORE').text,
                                    author=document.find('SOURCE_LABR_USER_ID').text,
                                    review=document.find('SOURCE_LABR_REVIEW_ID').text,
                                    book=document.find('SOURCE_LABR_BOOK_ID').text)
            rval.append(tmp)
    return rval


def load_and_serialize(corpus_path, pk_path):
    docs = load_corpus(corpus_path)
    print len(docs)
    with open(pk_path, 'w') as outfile:
        pk.dump(docs, outfile)


def main(argv):
    if len(argv) < 2:
        print "Usage: python xml_to_pk.py path/to/xml_corpus path/to/serialized_output"
        sys.exit(1)
    load_and_serialize(argv[0], argv[1])


if __name__ == '__main__':
    main(sys.argv[1:])
