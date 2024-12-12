
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

ReadOnlyBuffer = bytes | str
WritableBuffer = bytearray
Buffer = bytes | bytearray | str
Index = int
Size = int
FilesystemPath = Path
Matches = List[Index]


@dataclass
class Difference:
    a: ReadOnlyBuffer
    b: ReadOnlyBuffer
    size: Size
    index: Index


Differences = List[Difference]
Percentage = float
SimilarMatches = List[Tuple[Matches, Percentage]]
