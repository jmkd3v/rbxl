from __future__ import annotations
from typing import List, TYPE_CHECKING

from ...stream import RbxStream
from ...types.referent import Referent

if TYPE_CHECKING:
    from ..file import BinaryFile


class ParentChunk:
    def __init__(self, file: BinaryFile, stream: RbxStream):
        version: int = stream.read_int(1)
        assert version == 0, "Unknown version."

        self.version: int = version

        self.instance_count: int = stream.read_int(4)

        self.child_referents: List[Referent] = Referent.from_ints_accumulated(stream.read_interleaved_ints(
            length=4,
            count=self.instance_count,
            byteorder="big",
            signed=False,
            transform=True
        ))

        self.parent_referents: List[Referent] = Referent.from_ints_accumulated(stream.read_interleaved_ints(
            length=4,
            count=self.instance_count,
            byteorder="big",
            signed=False,
            transform=True
        ))

        assert len(self.child_referents) == self.instance_count, "child referent count did not match instance count"
        assert len(self.parent_referents) == self.instance_count, "parent referent count did not match instance count"
