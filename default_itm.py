import sys
import pipe
import oneline_to_pk as load
import tok
import rm_rare
import subsample as sub
import pk_to_itm as itm


def main(argv):
    assert len(argv) >= 3, "USAGE: python default_itm.py input/path output/path corpus_name"
    p = pipe.Pipe()
    p.add_step(load.OneDocPerLine())
    p.add_step(tok.Tokenizer())
    p.add_step(rm_rare.RareWordRemover())
    p.add_step(sub.Subsampler(n=100))
    p.add_step(itm.ItmOutputter(save=argv[1], name=argv[2]))
    with open(argv[0]) as infile:
        p.run(infile)


if __name__ == '__main__':
    main(sys.argv[1:])
