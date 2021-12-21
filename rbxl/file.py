from typing import List
from enum import Enum
from .chunks import Chunk, ChunkHeader, ChunkType


class FileType(Enum):
    binary = "binary"
    xml = "xml"


class Header:
    def __init__(self, data: bytes):
        magic: bytes = data[:8]
        assert magic == b"<roblox!"

        signature: bytes = data[8:14]
        assert signature == b"\x89\xFF\x0D\x0A\x1A\x0A"

        self.magic: bytes = magic
        self.signature: bytes = signature

        self.version: int = int.from_bytes(
            bytes=data[14:16],
            byteorder="little",
            signed=False
        )

        self.class_count: int = int.from_bytes(
            bytes=data[16:20],
            byteorder="little",
            signed=True
        )

        self.instance_count: int = int.from_bytes(
            bytes=data[20:24],
            byteorder="little",
            signed=True
        )

        self.reserved: bytes = data[24:32]


class BinaryFile:
    """
    Represents a Roblox binary file. These usually have the extension "rbxl" or "rbxm".
    """

    def __init__(self, data: bytes):
        self.data: bytes = data

        # header is length 32
        header_data = data[:32]
        chunks_data = data[32:]

        self.header: Header(header_data)
        self.chunks: List[Chunk] = []

        chunk_index = 0
        # while the index of the next chunk is not greater than the data length (sanity check)
        while len(chunks_data) > chunk_index:
            chunk_data_index = chunk_index + 16

            # header data fits snugly between the chunk start and the chunk data
            chunk_header_data = chunks_data[chunk_index:chunk_data_index]
            chunk_header = ChunkHeader(chunk_header_data)

            if chunk_header.compressed:
                chunk_data_length = chunk_header.compressed_size
            else:
                chunk_data_length = chunk_header.uncompressed_size

            # the end of the data is its start point + its length. That makes sense
            chunk_data_end = chunk_data_index + chunk_data_length

            chunk_compressed_data = chunks_data[chunk_data_index:chunk_data_end]

            if chunk_header.compressed:
                chunk_index += 16 + chunk_header.compressed_size
            else:
                chunk_index += 16 + chunk_header.uncompressed_size

            self.chunks.append(Chunk(
                header=chunk_header,
                compressed_data=chunk_compressed_data
            ))

            if chunk_header.type == ChunkType.end:
                # end chunks mark the end of the file. Break.
                break
