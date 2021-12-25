from io import BytesIO

from rbxl.binary.file import from_bytes
from rbxl.binary.chunks import ChunkType
from rbxl.binary.chunks.shared_string import SharedStringChunk
from rbxl.binary.chunks.property import PropertyChunk
from rbxl.binary.chunks.instance import InstanceChunk


def main():
    with open("./Baseplate.rbxl", "rb") as file:
        data = file.read()

    file = from_bytes(
        data=data
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

        with BytesIO() as file:
            file.write(data)
            file.seek(0)

            if chunk.header.type == ChunkType.property:
                property_chunk = PropertyChunk(file)
                print(f"\t\tName: {property_chunk.name}")
                print(f"\t\tClass ID: {property_chunk.class_id}")
                print(f"\t\tType: {property_chunk.type.name if property_chunk.type else '?'} [{property_chunk.type_id}]")
            elif chunk.header.type == ChunkType.shared_string:
                shared_string_chunk = SharedStringChunk(file)
                print(f"\t\tCount: {shared_string_chunk.count}")
                print(f"\t\tStrings:")
                for shared_string_index, shared_string in enumerate(shared_string_chunk.strings):
                    print(f"\t\t\tString {shared_string_index}:")
                    print(f"\t\t\t\tMD5: {shared_string.md5}")
                    print(f"\t\t\t\tLength: {len(shared_string.content)}")
                    print(f"\t\t\t\tContent: {shared_string.content!r}")
            elif chunk.header.type == ChunkType.instance:
                instance_chunk = InstanceChunk(file)
                print(f"\t\tClass name: {instance_chunk.class_name}")
                print(f"\t\tClass ID: {instance_chunk.class_id}")
                print(f"\t\tIs service: {instance_chunk.is_service}")
                print(f"\t\tInstance count: {instance_chunk.instance_count}")


if __name__ == '__main__':
    main()
