
from argparse import ArgumentParser
from pathlib import Path

from .diff import diffToJSONFile, readDifferencesJSONFile
from .io import readBytesFromPath, writeBytesToPath
from .patch import patchFromDifferences


def main() -> None:
    parser = ArgumentParser()

    parser.add_argument('-a', nargs=1, type=Path)
    parser.add_argument('-b', nargs=1, type=Path)
    parser.add_argument('-json', nargs=1, type=Path)

    parser.add_argument('--diff', action='store_true')
    parser.add_argument('--patch', action='store_true')

    args = parser.parse_args()

    if args.diff:
        aData = readBytesFromPath(args.a[0])
        bData = readBytesFromPath(args.b[0])
        jsonPath = args.json[0]

        diffToJSONFile(aData, bData, jsonPath)

    elif args.patch:
        aData = bytearray(readBytesFromPath(args.a[0]))
        differences = readDifferencesJSONFile(args.json[0])
        patched = patchFromDifferences(aData, differences)

        writeBytesToPath(args.b[0], patched)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
