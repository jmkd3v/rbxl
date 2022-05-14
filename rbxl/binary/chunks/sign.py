from __future__ import annotations
from typing import TYPE_CHECKING
from ...stream import RbxStream

if TYPE_CHECKING:
    from ..file import BinaryFile


class Signature:
    def __init__(self, stream: RbxStream):
        stream.skip(4)
        self.id: int = stream.read_int(4)
        stream.skip(4)
        size = stream.read_int(4)
        self.content: bytes = stream.read(size)


class SignChunk:
    def __init__(self, file: BinaryFile, stream: RbxStream):
        signature_count: int = stream.read_int(4)
        self.signatures: list[Signature] = []

        for _ in range(signature_count):
            self.signatures.append(Signature(stream))
