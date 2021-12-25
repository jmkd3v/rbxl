from rbxl import FileType, from_bytes
from rbxl import ChunkType
from rbxl import PropertyChunk
from rbxl import SharedStringChunk


def main():
    with open("./Baseplate.rbxl", "rb") as file:
        data = file.read()

    file = from_bytes(
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
        elif chunk.header.type == ChunkType.shared_string:
            shared_string_chunk = SharedStringChunk(data)
            print(f"\t\tCount: {shared_string_chunk.count}")
            print(f"\t\tStrings:")
            for shared_string_index, shared_string in enumerate(shared_string_chunk.strings):
                print(f"\t\t\tString {shared_string_index}:")
                print(f"\t\t\t\tMD5: {shared_string.md5}")
                print(f"\t\t\t\tLength: {len(shared_string.content)}")
                print(f"\t\t\t\tContent: {shared_string.content!r}")


if __name__ == '__main__':
    main()
