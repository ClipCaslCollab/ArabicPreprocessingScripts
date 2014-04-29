import argparse
import cPickle as pk
import os
import sys

import xml_to_pk
import oneline_to_pk
import tok
import subsample
import cv
import pk_to_itm
import pk_to_shlda


def load_ser_docs(inpath):
    print inpath
    with open(inpath) as infile:
        return pk.load(infile)
    return None


def arasent_import(intype, inpath, outpath):
    if intype == "xml":
        xml_to_pk.load_and_serialize(inpath, outpath)
    elif intype == "flat":
        oneline_to_pk.load_and_serialize(inpath, outpath)


def tokenize(inpath, outpath, lang):
    tok.tokenize_and_replace(load_ser_docs(inpath), outpath, lang)


def main_subsample(n, inpath, outpath):
    subsample.subsample_and_save(outpath, load_ser_docs(inpath), n)


def prep_cv(inpath, outpath, n, split):
    cv.prep_cv_and_save(load_ser_docs(inpath), outpath, n=n, split=split)


def export(cv, outype, inpath, outpath, name, lang):
    if outype == "itm":
        if cv:
            print "No notion of cross validation in itm"
        else:
            pk_to_itm.make_itm_input(load_ser_docs(inpath), outpath, name, lang=lang)
    elif outype == "shlda":
        if cv:
            pk_to_shlda.make_cv_shlda_input(inpath, outpath)
        else:
            pk_to_shlda.make_shlda_input(load_ser_docs(inpath), outpath, "arbooks")
    elif outype == "svml":
        print "Export to svm lite not implemented yet"
    elif outype == "mlt":
        print "Export to mallet format not implemented yet"


def main(argv):
    parser = argparse.ArgumentParser(description="Utilities for Arabic Sentiment Analysis")
    subparsers = parser.add_subparsers(dest="cmd", help="Commands")

    import_parser = subparsers.add_parser("import", help="Import files to IR")
    import_parser.add_argument("-t", dest="type", choices=["xml", "flat"], required=True)
    import_parser.add_argument("-o", dest="output", required=True, help="Output IR file")
    import_parser.add_argument("input", help="Input file")

    tok_parser = subparsers.add_parser("tok", help="Tokenize and morphologically analyze documents in IR format")
    tok_parser.add_argument("-l", dest="lang", choices=["en", "ar"], default="ar", help="Tokenization language.")
    tok_parser.add_argument("-o", dest="output", required=True, help="Output IR file")
    tok_parser.add_argument("input", help="Input IR file")

    subsample_parser = subparsers.add_parser("sub", help="Subsample corpus in IR format")
    subsample_parser.add_argument("-n", dest="num", type=int, required=True, help="Number of documents to sample")
    subsample_parser.add_argument("-o", dest="output", required=True, help="Output IR file")
    subsample_parser.add_argument("input", help="Input IR file")

    cv_parser = subparsers.add_parser("cv", help="Generate CV folds from IR format")
    cv_parser.add_argument("-n", dest="num", type=int, required=True, help="Number of folds")
    cv_parser.add_argument("-s", dest="split", type=float, required=True, help="Split [0, 1]")
    cv_parser.add_argument("-o", dest="output", required=True, help="Output directory")
    cv_parser.add_argument("input", help="Input IR file")

    export_parser = subparsers.add_parser("export", help="Export from IR to desired format")
    export_parser.add_argument("-c", dest="cv", action="store_true", help="Specify that input cross validation.")
    export_parser.add_argument("-l", dest="lang", default="ar", help="Language (en, ar)")
    export_parser.add_argument("-n", dest="name", default="arbooks", help="Corpus name")
    export_parser.add_argument("-o", dest="output", required=True, help="Output file or directory")
    export_parser.add_argument("-t", dest="type", choices=["itm", "shlda", "svml", "mlt"], required=True)
    export_parser.add_argument("input", help="Input IR file")

    arguments = parser.parse_args(argv)
    #print arguments

    if arguments.cmd == "import":
        arasent_import(arguments.type, arguments.input, arguments.output);
    elif arguments.cmd == "tok":
        tokenize(arguments.input, arguments.output, arguments.lang);
    elif arguments.cmd == "sub":
        main_subsample(arguments.num, arguments.input, arguments.output);
    elif arguments.cmd == "cv":
        prep_cv(arguments.input, arguments.output, arguments.num, arguments.split);
    elif arguments.cmd == "export":
        export(arguments.cv, arguments.type, arguments.input, arguments.output, arguments.name, arguments.lang);


if __name__ == '__main__':
    main(sys.argv[1:])
