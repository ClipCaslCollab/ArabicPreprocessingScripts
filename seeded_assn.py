import sys

def main(argv):
    if len(argv) < 1:
        print "USAGE: python seeded_assn.py ITM_MODEL_STATES"
    with open(argv[0]) as f:
        for line in f:
            #print line
            print " ".join(x.split(":")[0] for x in line.split())


if __name__ == '__main__':
    main(sys.argv[1:])
