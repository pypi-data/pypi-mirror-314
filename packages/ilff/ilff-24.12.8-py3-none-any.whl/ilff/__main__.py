import argparse

from . import __version__
from . import write, getline, getlines, nlines

def run():
    parser = argparse.ArgumentParser('ilff', description='ILFF file tool.')

    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')

    subparsers = parser.add_subparsers(title='Commands', dest='command')

    parser_a = subparsers.add_parser('getline')
    getline.setargs(parser_a)

    parser_a = subparsers.add_parser('write')
    write.setargs(parser_a)

#    parser_a = subparsers.add_parser('getlines')
#    nlines.setargs(parser_a)

    parser_a = subparsers.add_parser('nlines')
    nlines.setargs(parser_a)

    args = parser.parse_args()

    if args.command == 'write':
        write.exec(args)

    elif args.command == 'getline':
        getline.exec(args)

    elif args.command == 'nlines':
        nlines.exec(args)

if __name__ == "__main__":
    run()
