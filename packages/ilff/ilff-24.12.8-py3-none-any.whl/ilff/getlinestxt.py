import ilff
import sys

from .getlines import parseargs, getRange


def run():
    args = parseargs()

    (b, n) = getRange(args)

    fname = args.infile

    il = ilff.ILFFFile(fname)
    il.open()

    lns = il.getlinestxt(b, n)

    if args.outfile:
        of = open(args.outfile, 'w')
    else:
        of = sys.stdout

    of.write(lns)


if __name__ == "__main__":
    run()
