from typing import List, BinaryIO


class SharedString:
    def __init__(self, file: BinaryIO):
        md5_bytes = file.read(16)

        if len(md5_bytes) < 16:
            raise EOFError()

        self.md5: str = md5_bytes.decode("ascii")
        string_length = int.from_bytes(
            bytes=file.read(4),
            byteorder="little",
            signed=False
        )
        self.content: bytes = file.read(string_length)


class SharedStringChunk:
    def __init__(self, file: BinaryIO):
        version: int = int.from_bytes(
            bytes=file.read(4),
            byteorder="little",
            signed=False
        )

        assert version == 0, f"Unknown file version: {version}"

        self.version: int = version

        self.count: int = int.from_bytes(
            bytes=file.read(4),
            byteorder="little",
            signed=False
        )

        # TODO: improve this (it's a bit hacky passing entire data to string)
        self.strings: List[SharedString] = []

        while True:
            try:
                self.strings.append(SharedString(file))
            except EOFError:
                break
