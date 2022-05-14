from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from . import InstanceChunk
from ...stream import RbxStream
from ...types import DataType

if TYPE_CHECKING:
    from ..file import BinaryFile


class PropertyChunk:
    def __init__(self, file: BinaryFile, stream: RbxStream):
        self.class_id: int = stream.read_int(4)
        instance_chunk: InstanceChunk = file.class_id_to_chunk[self.class_id].contents
        instance_count = instance_chunk.instance_count

        self.name: str = stream.read_n_string("utf-8")

        self.type_id: int = stream.read_int(1)
        self.type: Optional[DataType]

        try:
            self.type = DataType(self.type_id)
        except ValueError:
            self.type = None

        self.values = None
        mapper = None

        if self.type == DataType.string:
            self.values = [stream.read_n() for _ in range(instance_count)]
        elif self.type == DataType.bool:
            self.values = [stream.read_bool() for _ in range(instance_count)]
        elif self.type == DataType.int32:
            self.values = stream.read_interleaved_ints(
                length=4,
                count=instance_count,
                signed=False,
                byteorder="big"
            )
