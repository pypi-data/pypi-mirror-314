import ilff
import sys
import argparse
from . import VERSION


def parseargs():
  parser = argparse.ArgumentParser(description='Get line range from ILFF file.')

  parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')

  #parser.add_argument('--debug', action='store_true', help='Debug output')
  #parser.add_argument('--verbose', action='store_true', help='Verbose output')

  group = parser.add_mutually_exclusive_group()
  group.add_argument('--begin', '-b', metavar='N', type=int, help='begin index')
  group.add_argument('--lines', '-l', type=str, metavar='M:N', help='line range begin:num')

  group = parser.add_mutually_exclusive_group()
  group.add_argument('--end', '-e', metavar='N', type=int, help='end index')
  group.add_argument('--number', '-n', metavar='N', type=int, help='number of lines')

  parser.add_argument('--sep', '-s', metavar='STR', type=str, help='record separator')
  parser.add_argument('--outfile', '-o', metavar='FILE', type=str, help='output file')

  parser.add_argument('infile', metavar='ILFF-File', type=str, help='input file name')

  args = parser.parse_args()
  return args


def getRange(args):
    b = None
    e = None
    n = None

    if args.lines:
        items = args.lines.split(':')
        if len(items) < 2:
            print('argument to -l must contain a colon (":")')
            sys.exit(1)

        [b, n] = [int(i) for i in items[0:2]]
    elif args.begin is None:
        print('-l or -b must be given')
        sys.exit(1)
    else:
        b = args.begin

        if args.end is not None:
            e = args.end
            n = e - b
        elif args.number is not None:
            n = args.number
        else:
            print('-n or -e must be given')
            sys.exit(1)

    return (b, n)


def run():
    args = parseargs()

    (b, n) = getRange(args)

    fname = args.infile

    il = ilff.ILFFFile(fname, sep=args.sep)
    il.open()

    lns = il.getlines(b, n)

    if args.outfile:
        of = open(args.outfile, 'w')
    else:
        of = sys.stdout

    of.write(''.join(lns))


if __name__ == "__main__":
    run()
