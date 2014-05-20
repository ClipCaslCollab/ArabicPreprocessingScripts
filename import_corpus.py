import csv
import codecs
import cPickle as pk
import cfg
import document
import re
import sys
import pipe
import xml.etree.ElementTree as ET


class OneDocPerLineLoader(pipe.Step):

    def load(self, infile):
        rval = []
        for line in infile:
            fields = line.split()
            tmp = document.Document(fields[0],
                                ' '.join(fields[2:]),
                                fields[1])
            rval.append(tmp)
        return rval


class XmlLoader(pipe.Step):
    BAD_XML = r'<SOURCELINK>.*</SOURCELINK>'

    def load(self, infile):
        rval = []
        text = '\n'.join(re.sub(self.BAD_XML, '', line) for line in infile)
        documents = ET.fromstring(text)
        for doc in documents:
            tmp = {}
            tmp = document.Document(doc.find('SOURCE_LABR_REVIEW_ID').text,
                                    doc.find('TEXT').text,
                                    doc.find('SCORE').text)
            rval.append(tmp)
        return rval


class CsvLoader(pipe.Step):

    def load(self, infile):
        reader = csv.DictReader(infile, delimiter=",")
        rval = []
        for row in reader:
            uid = row["doc_id"]
            text = row["doc_content"]
            score = row["doc_score"]
            rval.append(document.Document(uid, text, score))
        return rval


def load_corpus(corpus_path):
    rval = []
    with open(corpus_path, 'r') as infile:
        for line in infile:
            fields = line.split()
            tmp = document.Document(' '.join(fields[2:]),
                                fields[1],
                                uid=fields[0])
            rval.append(tmp)
    return rval


def load_and_serialize(corpus_path, pk_path):
    docs = load_corpus(corpus_path)
    with open(pk_path, 'w') as outfile:
        pk.dump(docs, outfile)


def main(argv):
    if len(argv) < 2:
        print "Usage: python oneline_to_pk.py path/to/oneline_per_file__corpus path/to/serialized_output"
        sys.exit(1)
    odl = OneDocPerLine(save=argv[1])
    with open(argv[0]) as infile:
        docs = odl.load(infile)
        docs = odl.xform(docs)
        odl.save(docs)


if __name__ == '__main__':
    main(sys.argv[1:])
