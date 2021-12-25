from enum import Enum
from typing import BinaryIO

import lz4.block


class ChunkType(Enum):
    shared_string = "SSTR"
    instance = "INST"
    property = "PROP"
    parent = "PRNT"
    end = "END"


class ChunkHeader:
    def __init__(self, file: BinaryIO):
        # string is null-terminated, so we split at the null byte
        self.name: str = file.read(4).split(b"\x00")[0].decode("ascii")
        self.type: ChunkType = ChunkType(self.name)

        self.compressed_size: int = int.from_bytes(
            bytes=file.read(4),
            byteorder="little",
            signed=False
        )

        self.uncompressed_size: int = int.from_bytes(
            bytes=file.read(4),
            byteorder="little",
            signed=False
        )

        self.compressed: bool = self.compressed_size != 0

        self.reserved: bytes = file.read(4)


class Chunk:
    def __init__(self, header: ChunkHeader, compressed_data: bytes):
        self.header: ChunkHeader = header
        self.compressed_data: bytes = compressed_data

    def decompress(self):
        return lz4.block.decompress(
            source=self.compressed_data,
            uncompressed_size=self.header.uncompressed_size
        )
