from io import BytesIO
from typing import List, BinaryIO

from .chunks import Chunk, ChunkHeader, ChunkType


class Header:
    def __init__(self, file: BinaryIO):
        magic: bytes = file.read(8)
        assert magic == b"<roblox!", "Invalid magic."

        signature: bytes = file.read(6)
        assert signature == b"\x89\xFF\x0D\x0A\x1A\x0A", "Invalid signature."

        version: int = int.from_bytes(
            bytes=file.read(2),
            byteorder="little",
            signed=False
        )
        assert version == 0, f"Unknown file version: {version}"

        self.magic: bytes = magic
        self.signature: bytes = signature
        self.version: int = version

        self.class_count: int = int.from_bytes(
            bytes=file.read(4),
            byteorder="little",
            signed=True
        )

        self.instance_count: int = int.from_bytes(
            bytes=file.read(4),
            byteorder="little",
            signed=True
        )

        self.reserved: bytes = file.read(8)


class BinaryFile:
    """
    Represents a Roblox binary file. These usually have the extension "rbxl" or "rbxm".
    """

    def __init__(self, file: BinaryIO):
        # header is length 32
        self.header: Header = Header(file)

        self.chunks: List[Chunk] = []

        while True:
            # header data fits snugly between the chunk start and the chunk data
            chunk_header = ChunkHeader(file)

            if chunk_header.compressed:
                chunk_data_length = chunk_header.compressed_size
            else:
                chunk_data_length = chunk_header.uncompressed_size

            # the end of the data is its start point + its length. That makes sense

            chunk_compressed_data = file.read(chunk_data_length)

            self.chunks.append(Chunk(
                header=chunk_header,
                compressed_data=chunk_compressed_data
            ))

            if chunk_header.type == ChunkType.end:
                # end chunks mark the end of the file. Break.
                break


def from_bytes(data: bytes):
    with BytesIO() as bytes_io:
        bytes_io.write(data)
        bytes_io.seek(0)
        return BinaryFile(bytes_io)
