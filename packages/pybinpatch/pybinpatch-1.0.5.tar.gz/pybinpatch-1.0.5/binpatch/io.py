
import json
from typing import Any

from .types import ReadOnlyBuffer, FilesystemPath, Size, Buffer


def readBytesFromPath(path: FilesystemPath) -> ReadOnlyBuffer:
    if not isinstance(path, FilesystemPath):
        raise TypeError('Path must be of type: FilesystemPath')

    if not path.is_file():
        raise TypeError('Path must be a file!')

    with open(path, 'rb') as f:
        return f.read()


def writeBytesToPath(path: FilesystemPath, data: Buffer) -> Size:
    if not isinstance(path, FilesystemPath):
        raise TypeError('Path must be of type: FilesystemPath')

    if path.is_file():
        raise FileExistsError('Path exists! Not overwriting!')

    with open(path, 'wb') as f:
        return f.write(data)


def readDataFromJSONFile(path: FilesystemPath) -> Any:
    if not isinstance(path, FilesystemPath):
        raise TypeError('Path must be of type: FilesystemPath')

    if not path.is_file():
        raise TypeError('Path must be a file!')

    with open(path) as f:
        return json.load(f)


def writeDataToJSONFile(path: FilesystemPath, data: Any, indent: Size = 2) -> None:
    if not isinstance(path, FilesystemPath):
        raise TypeError('Path must be of type: FilesystemPath')

    if path.is_file():
        raise FileExistsError('Path exists! Not overwriting!')

    with open(path, 'w') as f:
        json.dump(data, f, indent=indent)
