import rbxl
from rbxl.file import FileType


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


if __name__ == '__main__':
    main()
