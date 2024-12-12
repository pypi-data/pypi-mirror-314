
from binascii import hexlify

from .errors import NotEqualError
from .io import writeDataToJSONFile, readDataFromJSONFile
from .types import Difference, FilesystemPath, ReadOnlyBuffer, Differences


def diff(a: ReadOnlyBuffer, b: ReadOnlyBuffer) -> Differences:
    if not isinstance(a, ReadOnlyBuffer):
        raise TypeError('A must be of type: ReadOnlyBuffer')

    if not isinstance(b, ReadOnlyBuffer):
        raise TypeError('B must be of type: ReadOnlyBuffer')

    aSize = len(a)
    bSize = len(b)

    if aSize != bSize:
        raise NotEqualError(f'Size mismatch: a: {aSize}, b: {bSize}')

    aBuffer = bytearray()
    bBuffer = bytearray()

    lastPos = 0

    differences = []

    for i, (aValue, bValue) in enumerate(zip(a, b)):
        lastPos = i

        if aValue == bValue:
            if aBuffer and bBuffer:
                if len(aBuffer) != len(bBuffer):
                    raise NotEqualError('A and B buffer size mismatch!')

                difference = Difference(bytes(aBuffer), bytes(bBuffer), len(aBuffer), lastPos - len(aBuffer))
                differences.append(difference)

                aBuffer.clear()
                bBuffer.clear()

                continue
            else:
                continue

        aBuffer.append(aValue)
        bBuffer.append(bValue)

    return differences


def diffToJSONFile(a: ReadOnlyBuffer, b: ReadOnlyBuffer, path: FilesystemPath) -> None:
    if not isinstance(path, FilesystemPath):
        raise TypeError('Path must be of type: FilesystemPath')

    differences = diff(a, b)
    differencesJSON = {}

    for difference in differences:
        differencesJSON[hex(difference.index)] = {
            'a': hexlify(difference.a).decode(),
            'b': hexlify(difference.b).decode(),
            'size': hex(difference.size)
        }

    writeDataToJSONFile(path, differencesJSON)


def readDifferencesJSONFile(path: FilesystemPath) -> Differences:
    if not isinstance(path, FilesystemPath):
        raise TypeError('Path must be of type: FilesystemPath')

    differencesJSON = readDataFromJSONFile(path)
    differences = []

    for offset in differencesJSON:
        info = differencesJSON[offset]

        difference = Difference(
            b''.fromhex(info['a']),
            b''.fromhex(info['b']),
            int(info['size'], 16),
            int(offset, 16)
        )

        differences.append(difference)

    return differences
