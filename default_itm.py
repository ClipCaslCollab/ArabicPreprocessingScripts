import sys
import pipe
import import_corpus as load
import tok
import rm_rare
import subsample as sub
import export


def main(argv):
    assert len(argv) >= 3, "USAGE: python default_itm.py input/path output/path corpus_name"
    p = pipe.Pipe()
    p.add_step(load.OneDocPerLineLoader())
    p.add_step(sub.Subsampler(n=1000))
    p.add_step(tok.Tokenizer(lang="en"))
    p.add_step(rm_rare.RareWordRemover())
    p.add_step(export.ItmExporter(save=argv[1], name=argv[3]))
    print argv
    p.add_step(export.ShldaExporter(save=argv[2], name=argv[3]))
    with open(argv[0]) as infile:
        p.run(infile)


if __name__ == '__main__':
    main(sys.argv[1:])
