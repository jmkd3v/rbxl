from __future__ import annotations
from typing import List, TYPE_CHECKING

from ...stream import RbxStream

if TYPE_CHECKING:
    from ..file import BinaryFile


class SharedString:
    def __init__(self, stream: RbxStream):
        self.md5: str = stream.read_string(16)
        self.content: bytes = stream.read_n()


class SharedStringChunk:
    def __init__(self, file: BinaryFile, stream: RbxStream):
        version: int = stream.read_int(4)

        assert version == 0, f"Unknown file version: {version}"

        self.version: int = version

        count: int = stream.read_int(4)

        # TODO: improve this (it's a bit hacky passing entire data to string)
        self.strings: List[SharedString] = []

        for _ in range(count):
            self.strings.append(SharedString(stream))
