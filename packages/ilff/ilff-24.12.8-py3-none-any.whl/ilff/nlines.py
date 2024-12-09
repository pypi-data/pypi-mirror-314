import ilff
from . import VERSION
import sys
import argparse


def parseargs(help):
    parser = argparse.ArgumentParser(description='Get line range from ILFF file.')
    setargs(parser)
    return parser.parse_args()


def setargs(parser):
    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')
    parser.add_argument('infiles', metavar='ILFF-File', nargs='*', type=str, help='Input file')


def exec(args):
    for fname in args.infiles:
        il = ilff.ILFFFile(fname)
        il.open()
        if il.isILFF:
            print(fname, il.get_nlines())
        else:
            print(fname, "not an ILFF file")


def run():
    exec(parseargs('Get line range from ILFF file.'))


if __name__ == "__main__":
    run()
