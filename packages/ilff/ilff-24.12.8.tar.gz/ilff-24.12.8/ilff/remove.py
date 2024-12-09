import ilff
import sys
from .nlines import parseargs


def run():
    args = parseargs('Delete ILFF files including the index.')
    for fname in args.infiles:
        il = ilff.ILFFFile(fname, mode='w')
        il.remove()


if __name__ == "__main__":
    run()

