
from binpatch.errors import NotEqualError
from .types import WritableBuffer, Differences
from .utils import getBufferAtIndex, replaceBufferAtIndex


def patchFromDifferences(data: WritableBuffer, differences: Differences) -> WritableBuffer:
    if not isinstance(data, WritableBuffer):
        raise TypeError('Data must be of type: WritableBuffer')

    for difference in differences:
        buffer = getBufferAtIndex(data, difference.index, difference.size)

        if buffer != difference.a:
            raise NotEqualError('A attribute not the same!')

        data = replaceBufferAtIndex(data, difference.b, difference.index, difference.size)

    return data
