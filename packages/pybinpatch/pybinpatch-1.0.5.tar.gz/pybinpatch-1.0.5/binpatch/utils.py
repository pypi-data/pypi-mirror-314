
from .errors import EmptyError, ZeroError, NotEqualError
from .types import Buffer, Index, Size


def getBufferAtIndex(data: Buffer, index: Index, length: Size) -> Buffer:
    if not isinstance(data, Buffer):
        raise TypeError('Data must be of type: Buffer')

    if not data:
        raise EmptyError('Data is empty!')

    if not isinstance(index, Index):
        raise TypeError('Index must be of type: Index')

    if index not in range(len(data)):
        raise IndexError(f'Bad index: {index}')

    if not isinstance(length, Size):
        raise TypeError('Length must be of type: Size')

    if length == 0:
        raise ZeroError('Length must not be 0!')

    buffer = data[index:index+length]

    if not buffer:
        raise EmptyError('Buffer is empty!')

    buffer_len = len(buffer)

    if buffer_len != length:
        raise NotEqualError(f'Buffer length mismatch! Got {buffer_len}')

    return buffer


def replaceBufferAtIndex(data: Buffer, pattern: Buffer, index: Index, length: Size) -> Buffer:
    if not isinstance(data, Buffer):
        raise TypeError('Data must be of type: Buffer')

    if not isinstance(pattern, Buffer):
        raise TypeError('Pattern must be of type: Buffer')

    if isinstance(data, str) and not isinstance(pattern, str):
        raise TypeError('Data IS str but pattern IS NOT!')

    if not isinstance(data, str) and isinstance(pattern, str):
        raise TypeError('Data IS NOT str but pattern IS!')

    isStr = False

    if isinstance(data, str) and isinstance(pattern, str):
        isStr = True

    if len(pattern) != length:
        raise NotEqualError('Pattern must be the same size as length!')

    buffer = getBufferAtIndex(data, index, length)

    if buffer == pattern:
        return data

    if isStr:
        dataFront = getBufferAtIndex(data, 0, index)
        dataBack = getBufferAtIndex(data, index + length, len(data) - length - index)
        data = ''.join((dataFront, pattern, dataBack))

    else:
        data[index:index+length] = pattern

    patchedBuffer = getBufferAtIndex(data, index, length)

    if patchedBuffer != pattern:
        raise ValueError('Failed to replace buffer!')

    return data
