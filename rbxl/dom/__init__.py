from __future__ import annotations
from io import BytesIO

from enum import Enum
from typing import Optional, Dict, BinaryIO, List

from .instance import Instance
from ..types.referent import Referent

from ..binary.file import BinaryFile

from ..binary.chunks import ChunkType
from ..binary.chunks.shared_string import SharedStringChunk
from ..binary.chunks.instance import InstanceChunk
from ..binary.chunks.property import PropertyChunk
from ..binary.chunks.parent import ParentChunk


class RobloxFileType(Enum):
    xml = "xml"
    binary = "binary"


class RobloxDOM:
    def __init__(self):
        self.referents = []

        self.root_referent: Referent = Referent(-1)
        self.root_instance: Instance = Instance(
            referent=self.root_referent,
            class_name="DataModel"
        )

        self._referent_to_instance: Dict[Referent, Instance] = {}
        self._class_id_to_referents: Dict[int, List[Referent]] = {}

    def get_instance_from_referent(self, referent: Referent):
        if referent.value == -1:
            return self.root_instance
        else:
            return self._referent_to_instance[referent]

    @classmethod
    def from_file(cls, file: BinaryIO, file_type: Optional[RobloxFileType] = None) -> RobloxDOM:
        self = cls()

        if file_type is None:
            start_point = file.tell()
            start_header = file.read(8)
            file.seek(start_point)

            if start_header == b"<roblox!":
                file_type = RobloxFileType.binary
            else:
                file_type = RobloxFileType.xml

        if file_type == RobloxFileType.binary:
            file = BinaryFile(file)
            self._load_binaryfile(file)
        else:
            raise NotImplementedError("XML is not implemented!")

        return self

    def _load_binaryfile(self, file: BinaryFile):
        property_chunks = []
        instance_chunks = []
        parent_chunk: Optional[ParentChunk] = None
        shared_string_chunk: Optional[SharedStringChunk] = None

        for chunk in file.chunks:
            if chunk.header.compressed:
                data = chunk.decompress()
            else:
                data = chunk.compressed_data

            with BytesIO() as file:
                file.write(data)
                file.seek(0)

                if chunk.header.type == ChunkType.property:
                    property_chunks.append(PropertyChunk(file))
                elif chunk.header.type == ChunkType.instance:
                    instance_chunks.append(InstanceChunk(file))
                elif chunk.header.type == ChunkType.shared_string:
                    shared_string_chunk = SharedStringChunk(file)
                elif chunk.header.type == ChunkType.parent:
                    parent_chunk = ParentChunk(file)

        assert parent_chunk, "Malformed file! No parent chunk present."
        assert shared_string_chunk, "Malformed file! No shared string chunk present."

        for instance_chunk in instance_chunks:
            for referent in instance_chunk.referents:
                instance = self._referent_to_instance.get(referent)

                if instance:
                    continue

                instance = Instance(
                    referent=referent,
                    class_name=instance_chunk.class_name
                )

                self._referent_to_instance[referent] = instance

                referents_list = self._class_id_to_referents.get(instance_chunk.class_id)

                if referents_list is None:
                    referents_list = []
                    self._class_id_to_referents[instance_chunk.class_id] = referents_list

                referents_list.append(referent)

        for property_chunk in property_chunks:
            referents_list = self._class_id_to_referents.get(property_chunk.class_id)
            if referents_list:
                for referent in referents_list:
                    instance = self._referent_to_instance[referent]

                    instance.set_property(
                        name=property_chunk.name,
                        value=property_chunk.raw_value
                    )

        for referent_index in range(parent_chunk.instance_count):
            parent_referent = parent_chunk.parent_referents[referent_index]
            child_referent = parent_chunk.child_referents[referent_index]

            parent_instance = self.get_instance_from_referent(parent_referent)
            child_instance = self.get_instance_from_referent(child_referent)

            child_instance.parent_referent = parent_referent
            parent_instance.children_referents.append(child_referent)
