from typing import BinaryIO, List

from ...types.referent import Referent


class InstanceChunk:
    def __init__(self, file: BinaryIO):
        self.class_id: int = int.from_bytes(
            bytes=file.read(4),
            byteorder="little",
            signed=False
        )

        name_length = int.from_bytes(
            bytes=file.read(4),
            byteorder="little",
            signed=False
        )
        self.class_name: str = file.read(name_length).decode("utf-8")

        self.is_service: bool = int.from_bytes(
            bytes=file.read(1),
            byteorder="little",
            signed=False
        ) == 1

        self.instance_count: int = int.from_bytes(
            bytes=file.read(4),
            byteorder="little",
            signed=False
        )

        self.referents: List[Referent] = []

        for _ in range(self.instance_count):
            referent_bytes = file.read(16)
            print(referent_bytes)
            if len(referent_bytes) < 16:
                break
            self.referents.append(Referent.from_bytes(referent_bytes))
