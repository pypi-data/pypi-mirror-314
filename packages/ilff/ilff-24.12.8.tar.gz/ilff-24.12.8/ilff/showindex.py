import ilff
import sys
from .nlines import parseargs


def run():
    args = parseargs('Show index of ILFF file.')
    for fname in args.infiles:
        il = ilff.ILFFFile(fname)
        il.open()
        il.dumpindex()


if __name__ == "__main__":
    run()
