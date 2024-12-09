import ilff
from . import VERSION

import sys
import argparse


def parseargs(cmdargs=None):
    parser = argparse.ArgumentParser(description='Concatenate ILFF files.')

    parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')

    parser.add_argument('--verbose', type=int, nargs='?', const=1, help='Verbose output')
    parser.add_argument('--outfile', '-o', type=str, help='Output ILFF file')

    parser.add_argument('infile', type=str, nargs='*', help='Input files')


    args = parser.parse_args(cmdargs)

    return args


def run():

    args = parseargs()

    ofile = args.outfile
    if ofile is None:
        print('Output file must be set')
        return
    else:
        il = ilff.ILFFFile(ofile, 'w')
        il.open()
        ofile = il

    infiles = args.infile
    if len(infiles) == 0:
        infiles = [sys.stdin]

    for i in infiles:
        try:
            f = open(i, 'r') if isinstance(i, str) else i
        except FileNotFoundError as ex:
            print(f'Failed to open input: {ex}')
            break
        with f:
            ofile.fromfile(f, empty=None)


if __name__ == "__main__":
    run()
