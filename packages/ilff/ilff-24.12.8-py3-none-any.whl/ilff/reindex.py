import ilff
import sys
from .nlines import parseargs


def run():
    args = parseargs('Refresh index of ILFF file')
    for fname in args.infiles:
        with ilff.ILFFFile(fname, mode='a+', check=False) as il:
            il.buildindex()


if __name__ == "__main__":
    run()

