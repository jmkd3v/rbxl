from typing import List


class SharedString:
    def __init__(self, data: bytes):
        self.md5: str = data[:16].decode("ascii")
        string_length = int.from_bytes(
            bytes=data[16:20],
            byteorder="little",
            signed=False
        )
        self.content: bytes = data[20:20 + string_length]


class SharedStringChunk:
    def __init__(self, data: bytes):
        self.data: bytes = data
        self.version: int = int.from_bytes(
            bytes=data[:4],
            byteorder="little",
            signed=False
        )
        self.count: int = int.from_bytes(
            bytes=data[4:8],
            byteorder="little",
            signed=False
        )

        # TODO: improve this (it's a bit hacky passing entire data to string)
        self.strings: List[SharedString] = []

        shared_strings_data = data[8:]
        shared_string_index = 0
        while shared_string_index < len(shared_strings_data):
            shared_string = SharedString(shared_strings_data[shared_string_index:])
            shared_string_index += len(shared_string.content) + 20
            self.strings.append(shared_string)
