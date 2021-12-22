from pathlib import Path
import rbxl
from rbxl.file import FileType
from rbxl.chunks import ChunkType
from rbxl.chunks.property import PropertyChunk


def main():
    with open("./Baseplate.rbxl", "rb") as file:
        data = file.read()

    file = rbxl.from_bytes(
        data=data,
        file_type=FileType.binary
    )

    for i, chunk in enumerate(file.chunks):
        chunk_header = chunk.header
        print(f"Chunk {i}:")
        print(f"\tType: {chunk_header.type}")
        print(f"\tCompressed: {chunk_header.compressed}")
        print(f"\tCompressed length: {chunk_header.compressed_size}")
        print(f"\tUncompressed length: {chunk_header.uncompressed_size}")

        if chunk.header.compressed:
            data = chunk.decompress()
        else:
            data = chunk.compressed_data

        if chunk.header.type == ChunkType.property:
            property_chunk = PropertyChunk(data)
            print(f"\t\tName: {property_chunk.name}")
            print(f"\t\tClass ID: {property_chunk.class_id}")
            print(f"\t\tType: {property_chunk.type.name if property_chunk.type else '?'} [{property_chunk.type_id}]")


if __name__ == '__main__':
    main()
