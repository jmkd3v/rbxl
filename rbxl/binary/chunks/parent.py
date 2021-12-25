from typing import BinaryIO, List

from ...types.referent import Referent
from ..interleaving import deinterleave_int


class ParentChunk:
    def __init__(self, file: BinaryIO):
        version: int = int.from_bytes(
            bytes=file.read(1),
            byteorder="little",
            signed=False
        )
        assert version == 0, "Unknown version."

        self.version: int = version

        self.instance_count: int = int.from_bytes(
            bytes=file.read(4),
            byteorder="little",
            signed=False
        )

        a = file.read(self.instance_count * 4)
        b = file.read(self.instance_count * 4)

        print(a)
        print(b)

        self.child_referents: List[Referent] = Referent.from_ints_accumulated(deinterleave_int(a))
        self.parent_referents: List[Referent] = Referent.from_ints_accumulated(deinterleave_int(b))

        assert len(self.child_referents) == self.instance_count, "Child referent count did not match instance count."
        assert len(self.parent_referents) == self.instance_count, "Parent referent count did not match instance count."
