from typing import BinaryIO, List

from ...types.referent import Referent
from ..interleaving import deinterleave_int


class InstanceChunk:
    def __init__(self, file: BinaryIO):
        self.class_id: int = int.from_bytes(
            bytes=file.read(4),
            byteorder="little",
            signed=False
        )

        name_length = int.from_bytes(
            bytes=file.read(4),
            byteorder="little",
            signed=False
        )
        self.class_name: str = file.read(name_length).decode("utf-8")

        self.is_service: bool = int.from_bytes(
            bytes=file.read(1),
            byteorder="little",
            signed=False
        ) == 1

        self.instance_count: int = int.from_bytes(
            bytes=file.read(4),
            byteorder="little",
            signed=False
        )

        self.referents: List[Referent] = []
        self.markers: List[bool] = []

        self.referents = Referent.from_ints_accumulated(deinterleave_int(
            data=file.read(4 * self.instance_count)
        ))

        assert len(self.referents) == self.instance_count, "Referent count did not match instance count."
