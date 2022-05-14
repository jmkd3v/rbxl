from io import BytesIO

from .chunks import Chunk, ChunkType
from ..stream import RbxStream


class Header:
    def __init__(self, stream: RbxStream):
        assert stream.read(8) == b"<roblox!", "invalid magic."
        assert stream.read(6) == b"\x89\xFF\x0D\x0A\x1A\x0A", "invalid signature"
        assert stream.read_int(2) == 0, f"unknown file version"

        self.class_count: int = stream.read_int(4)
        self.instance_count: int = stream.read_int(4)

        stream.skip(8)


class BinaryFile:
    """
    Represents a Roblox binary file. These usually have the extension "rbxl" or "rbxm".
    """

    def __init__(self, stream: RbxStream):
        # header is length 32
        self.header: Header = Header(stream)

        self.chunks: list[Chunk] = []
        self.class_id_to_chunk: dict[int, Chunk] = {}

        while True:
            chunk = Chunk(self, stream)

            if chunk.type == ChunkType.instance:
                self.class_id_to_chunk[chunk.contents.class_id] = chunk
            elif chunk.type == ChunkType.end:
                # end chunks mark the end of the file. Break.
                break

            self.chunks.append(chunk)

        print(self.class_id_to_chunk)

    @classmethod
    def from_bytes(cls, data: bytes):
        with BytesIO() as bytes_io:
            bytes_io.write(data)
            bytes_io.seek(0)
            stream = RbxStream(stream=bytes_io)
            return cls(stream)
