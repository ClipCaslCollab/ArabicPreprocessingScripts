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

