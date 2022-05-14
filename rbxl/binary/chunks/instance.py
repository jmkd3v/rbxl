from __future__ import annotations
from typing import List, TYPE_CHECKING

from ...stream import RbxStream
from ...types.referent import Referent


if TYPE_CHECKING:
    from ..file import BinaryFile


class InstanceChunk:
    def __init__(self, file: BinaryFile, stream: RbxStream):
        self.class_id: int = stream.read_int(4)

        name_length = stream.read_int(4)
        self.class_name: str = stream.read_string(name_length, "utf-8")

        self.is_service: bool = stream.read_bool()

        self.instance_count: int = stream.read_int(4)

        self.referents: List[Referent] = []
        self.markers: List[bool] = []

        self.referents = Referent.from_ints_accumulated(stream.read_interleaved_ints(
            length=4,
            count=self.instance_count,
            byteorder="big",
            transform=True
        ))

        assert len(self.referents) == self.instance_count, "Referent count did not match instance count."
