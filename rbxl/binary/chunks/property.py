from typing import Optional

from ..datatypes import DataType


class PropertyChunk:
    def __init__(self, data: bytes):
        self.data: bytes = data
        self.class_id: int = int.from_bytes(
            bytes=data[:4],
            byteorder="little",
            signed=False
        )

        name_length = int.from_bytes(
            bytes=data[4:8],
            byteorder="little",
            signed=False
        )
        name_end = 8 + name_length
        self.name: str = data[8:name_end].decode("utf-8")

        self.type_id: int = int.from_bytes(
            bytes=data[name_end:name_end + 1],
            byteorder="little",
            signed=False
        )

        self.type: Optional[DataType]

        try:
            self.type = DataType(self.type_id)
        except ValueError:
            self.type = None
