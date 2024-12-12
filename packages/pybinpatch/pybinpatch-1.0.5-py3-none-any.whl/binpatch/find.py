
from difflib import SequenceMatcher

from .types import Buffer, ReadOnlyBuffer, Matches, Percentage, SimilarMatches
from .utils import getBufferAtIndex


class Finder:
    def __init__(self, data: Buffer, pattern: ReadOnlyBuffer) -> None:
        self._data = data
        self._dataSize = len(self._data)
        self._pattern = pattern
        self._patternSize = len(self._pattern)
        self._searchSize = self._dataSize - self._patternSize + 1
        self.table = self.makeTable()

    def makeTable(self) -> dict:
        table = {}

        for i in range(0, self._searchSize, self._patternSize):
            buffer = getBufferAtIndex(self._data, i, self._patternSize)
            bufferHash = hash(buffer)

            if bufferHash not in table:
                table[bufferHash] = {
                    'data': buffer,
                    'matches': []
                }

            table[bufferHash]['matches'].append(i)

        return table

    def findExactMatch(self) -> Matches | None:
        matches = None

        for bufferHash in self.table:
            buffer = self.table[bufferHash]['data']

            if buffer != self._pattern:
                continue

            matches = self.table[bufferHash]['matches']
            break

        return matches

    def findSimilarMatch(self, minMatch: Percentage = .5) -> SimilarMatches:
        if not isinstance(minMatch, Percentage):
            raise TypeError('minMatch must be of type: Percentage')

        matches = []
        matcher = SequenceMatcher()
        matcher.set_seq2(self._pattern)

        for bufferHash in self.table:
            buffer = self.table[bufferHash]['data']
            matcher.set_seq1(buffer)
            ratio = matcher.ratio()

            if ratio < minMatch:
                continue

            match = (
                self.table[bufferHash]['matches'],
                ratio
            )
            matches.append(match)

        return matches
