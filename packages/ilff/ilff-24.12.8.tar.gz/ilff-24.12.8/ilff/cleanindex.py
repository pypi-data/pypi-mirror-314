import ilff
from . import VERSION
import sys
import os
import argparse


def parseargs():
  parser = argparse.ArgumentParser(description='Delete all ILFF indices in directory.')

  parser.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')

  parser.add_argument('dir', nargs='*', type=str, help='directory')

  args = parser.parse_args()
  return args


def run():
    args = parseargs()

    for base in args.dir:
        indexDir = os.path.join(base, '.ilff-index')

        files = [f for f in os.listdir(indexDir) if os.path.isfile(os.path.join(indexDir, f))]

        for indexFile in files:
            if indexFile.endswith('.idx'):
                fullname = os.path.join(indexDir, indexFile)
                mainname = indexFile[:-4]
                if not os.path.isfile(os.path.join(base, mainname)):
                    print(f'stale index {fullname}')
                    os.remove(fullname)


if __name__ == "__main__":
    run()
