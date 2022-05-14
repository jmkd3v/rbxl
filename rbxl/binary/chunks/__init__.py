from __future__ import annotations

from enum import Enum
from io import BytesIO
from typing import TYPE_CHECKING

import lz4.block

from .instance import InstanceChunk
from .parent import ParentChunk
from .property import PropertyChunk
from .shared_string import SharedStringChunk
from .sign import SignChunk
from ...stream import RbxStream

if TYPE_CHECKING:
    from ..file import BinaryFile


class ChunkType(Enum):
    shared_string = "SSTR"
    instance = "INST"
    property = "PROP"
    parent = "PRNT"
    sign = "SIGN"
    end = "END"


_chunk_type_to_class = {
    ChunkType.shared_string: SharedStringChunk,
    ChunkType.instance: InstanceChunk,
    ChunkType.property: PropertyChunk,
    ChunkType.parent: ParentChunk,
    ChunkType.sign: SignChunk
}


class Chunk:
    def __init__(self, file: BinaryFile, stream: RbxStream):
        self._file = file
        self.type: ChunkType = ChunkType(stream.read_string(4).strip("\x00"))

        self.compressed_size: int = stream.read_int(4)
        self.uncompressed_size: int = stream.read_int(4)

        self.compressed: bool = self.compressed_size != 0
        stream.skip(4)

        contents_class = _chunk_type_to_class.get(self.type)

        if not contents_class:
            self.contents = None
            return

        chunk_stream = None
        needs_closing = False

        if self.compressed:
            # for compressed data, we need to decompress the data and wrap it in a RbxStream
            needs_closing = True
            self.data = lz4.block.decompress(
                source=stream.read(self.compressed_size),
                uncompressed_size=self.uncompressed_size
            )
            chunk_stream = RbxStream(
                stream=BytesIO(self.data)
            )
        else:
            # for uncompressed data, we don't need to make a new stream at all
            self.data = stream.read(self.uncompressed_size)
            stream.seek(stream.tell() - self.uncompressed_size)
            chunk_stream = stream

        self.contents = contents_class(self._file, chunk_stream)

        if needs_closing:
            chunk_stream.stream.close()
