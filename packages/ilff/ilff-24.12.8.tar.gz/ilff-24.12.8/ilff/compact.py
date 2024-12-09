import ilff
from .nlines import parseargs
import sys


def run():
    args = parseargs('Remove emoty lines from ILFF file.')
    empty = ''
    for fname in args.infiles:
        il = ilff.ILFFFile(fname, mode='r+')
        il.open()
        il.compact(empty=empty)
        il.close()


if __name__ == "__main__":
    run()

