from typing import BinaryIO, Optional

from ...types import DataType


class PropertyChunk:
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
        self.name: str = file.read(name_length).decode("utf-8")

        self.type_id: int = int.from_bytes(
            bytes=file.read(1),
            byteorder="little",
            signed=False
        )

        self.type: Optional[DataType]

        try:
            self.type = DataType(self.type_id)
        except ValueError:
            self.type = None

        self.raw_value: bytes = file.read()
