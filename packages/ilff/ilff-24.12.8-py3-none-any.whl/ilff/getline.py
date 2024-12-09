import ilff
import sys
import argparse
from . import VERSION


def setargs(parser):
    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')

    parser.add_argument('infile', metavar='ILFF-File', type=str, help='input file name')
    parser.add_argument('line', metavar='Number', type=int, nargs='+', help='line number')

    parser.add_argument('--outfile', '-o', metavar='FILE', type=str, help='output file')


def run():
    parser = argparse.ArgumentParser(description='Get line(s) from ILFF file.')
    setargs(parser)
    args = parser.parse_args()
    exec(args)

def exec(args):
    fname = args.infile

    il = ilff.ILFFFile(fname)
    il.open()
    if not il.isILFF:
        print(f'{fname} is not an ILFF-File')
        sys.exit(1)

    if args.outfile:
        of = open(args.outfile, 'w')
    else:
        of = sys.stdout

    for ln in args.line:
        l = il.getline(ln)
        of.write(l)


if __name__ == "__main__":
    run()
