import os
import unittest

import cfg
import document
import import_corpus
import export


class TestImporters(unittest.TestCase):

    class FakeFile(object):

        def __init__(self, lines):
            self._i = 0
            self._lines = lines

        def read(self):
            rval = '\n'.join(lines[self._i:])
            self._i = len(self._lines)
            return rval

        def next(self):
            if self._i >= len(self._lines):
                raise StopIteration()
            rval = self._lines[self._i]
            self._i += 1
            return rval

        def close(self):
            pass

        def __iter__(self):
            return self

    def run_import_tests(self, step, f):
        docs = step.load(f)
        self.assertEqual(len(docs), 3)
        self.assertEqual(docs[0].unique_id, '0')
        self.assertEqual(docs[1].unique_id, '1')
        self.assertEqual(docs[2].unique_id, '2')
        for doc in docs:
            self.assertEquals(doc.text, "text text text")
        self.assertEqual(docs[0].score, '1')
        self.assertEqual(docs[1].score, '2')
        self.assertEqual(docs[2].score, '3')

    def test_onedoc_import(self):
        f = self.FakeFile(["0 1 text text text",
            "1 2 text text text",
            "2 3 text text text"])
        self.run_import_tests(import_corpus.OneDocPerLineLoader(), f)

    def test_csv_import(self):
        f = self.FakeFile(["doc_id,doc_content,doc_score",
            "0,text text text,1",
            "1,text text text,2",
            "2,text text text,3"])
        self.run_import_tests(import_corpus.CsvLoader(), f)

    def test_xml_import(self):
        f = self.FakeFile(["<DOCUMENTS>",
            "<DOCUMENT>",
                "<SCORE>1</SCORE>",
                "<TEXT>text text text</TEXT>",
                "<SOURCE_LABR_REVIEW_ID>0</SOURCE_LABR_REVIEW_ID>",
            "</DOCUMENT>",
            "<DOCUMENT>",
                "<SCORE>2</SCORE>",
                "<TEXT>text text text</TEXT>",
                "<SOURCE_LABR_REVIEW_ID>1</SOURCE_LABR_REVIEW_ID>",
            "</DOCUMENT>",
            "<DOCUMENT>",
                "<SCORE>3</SCORE>",
                "<TEXT>text text text</TEXT>",
                "<SOURCE_LABR_REVIEW_ID>2</SOURCE_LABR_REVIEW_ID>",
            "</DOCUMENT>",
            "</DOCUMENTS>"])
        self.run_import_tests(import_corpus.XmlLoader(), f)


class TestExporters(unittest.TestCase):

    def setUp(self):
        self.docs = [document.Document("0", "text text text", "1"),
            document.Document("1", "text text text", "2"),
            document.Document("2", "text text text", "3")]

    def test_itm_export(self):
        path = os.path.join(cfg.SCRATCH_PATH, "test_itm")
        step = export.ItmExporter(save=path, name="test")
        step.save(self.docs)
        self.assertTrue(os.path.isdir(os.path.join(path, 'results')))
        self.assertTrue(os.path.isdir(os.path.join(path, 'results', 'test')))
        self.assertTrue(os.path.isdir(os.path.join(path, 'results', 'test', 'input')))
        self.assertTrue(os.path.isfile(os.path.join(path, 'results', 'test', 'input', 'test-topic-input.mallet')))
        self.assertTrue(os.path.isfile(os.path.join(path, 'results', 'test', 'input', 'test.url')))
        self.assertTrue(os.path.isfile(os.path.join(path, 'results', 'test', 'input', 'tree_hyperparams')))
        self.assertTrue(os.path.isdir(os.path.join(path, 'results', 'test', 'output')))
        self.assertTrue(os.path.isdir(os.path.join(path, 'data')))
        self.assertTrue(os.path.isfile(os.path.join(path, 'data', 'test.html')))

    def test_itm_export(self):
        path = os.path.join(cfg.SCRATCH_PATH, "test_shlda")
        step = export.ShldaExporter(save=path, name="test")
        step.save(self.docs)
        self.assertTrue(os.path.isdir(os.path.join(path, 'test')))
        self.assertTrue(os.path.isdir(os.path.join(path, 'test', 'format')))
        self.assertTrue(os.path.isfile(os.path.join(path, 'test', 'format', 'test.dat')))
        self.assertTrue(os.path.isfile(os.path.join(path, 'test', 'format', 'test.docinfo')))
        self.assertTrue(os.path.isfile(os.path.join(path, 'test', 'format', 'test.sent-dat')))
        self.assertTrue(os.path.isfile(os.path.join(path, 'test', 'format', 'test.sent-dat.raw')))
        self.assertTrue(os.path.isfile(os.path.join(path, 'test', 'format', 'test.wvoc')))
        self.assertTrue(os.path.isdir(os.path.join(path, 'test', 'raw')))


if __name__ == '__main__':
    unittest.main()
