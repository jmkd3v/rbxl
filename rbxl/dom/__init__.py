from __future__ import annotations

import warnings

from bs4 import BeautifulSoup
from bs4.element import Tag
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

from ..xml import element_name_to_handler


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
            soup = BeautifulSoup(
                markup=file.read().decode("utf-8"),
                features="lxml-xml"
            )
            self._load_soup(soup)

        return self

    def _load_soup(self, soup: BeautifulSoup):
        roblox_tag = soup.find("roblox")
        assert roblox_tag.get("version") == "4"

        def iterate_item_children(item_tag, item_instance: Instance):
            child_tags = item_tag.find_all(
                name="Item",
                recursive=False
            )

            for i, child_tag in enumerate(child_tags):
                child_referent = Referent.from_hex(child_tag.get("referent")[3:])

                child_instance = Instance(
                    class_name=child_tag.get("class"),
                    referent=child_referent
                )

                properties_el = item_tag.find("Properties", recursive=False)
                if properties_el:
                    for property_el in properties_el.contents:
                        if not isinstance(property_el, Tag):
                            continue

                        property_type = property_el.name
                        property_name = property_el.get("name")
                        property_type_handler = element_name_to_handler.get(property_type)

                        if property_type_handler:
                            property_value = property_type_handler(property_el)
                        else:
                            warnings.warn(f"Unknown type: {property_type}")
                            property_value = property_el.get_text()

                        child_instance.set_property(property_name, property_value)
                # print(f"\t\tSet props")

                child_instance.parent_referent = item_instance.referent
                # print(f"\t\tSet parent ref to {item_instance.referent} ({item_instance.class_name})")
                item_instance.children_referents.append(child_referent)
                # print(f"\t\tAppended child_ref to {item_instance.referent} ({item_instance.class_name})")
                self._referent_to_instance[child_referent] = child_instance
                # print(f"\t\tAdded ref {child_referent} to index.")

                iterate_item_children(
                    item_tag=child_tag,
                    item_instance=child_instance
                )
            # print(f"Done iterating through {item_instance.class_name}")

        iterate_item_children(roblox_tag, self.root_instance)

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

    def to_soup(self) -> BeautifulSoup:
        soup = BeautifulSoup("", "lxml-xml")
        soup.is_xml = False

        roblox_tag = soup.new_tag(
            name="roblox",
            attrs={
                "version": "4",
                "xmlns:xmime": "http://www.w3.org/2005/05/xmlmime",
                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "xsi:noNamespaceSchemaLocation": "http://www.roblox.com/roblox.xsd"
            }
        )

        external_null_tag = soup.new_tag("External")
        external_null_tag.append("null")

        external_nil_tag = soup.new_tag("External")
        external_nil_tag.append("nil")

        roblox_tag.append(external_null_tag)
        roblox_tag.append(external_nil_tag)

        def instance_to_tag(instance: Instance):
            instance_tag = soup.new_tag(
                name="Item",
                attrs={
                    "class": instance.class_name,
                    "referent": instance.referent.to_hex()
                }
            )

            properties_tag = soup.new_tag("Properties")

            for property_name, property_value in instance.get_properties():
                property_tag = soup.new_tag(
                    name="?",
                    attrs={
                        "name": property_name
                    }
                )
                property_tag.append(str(property_value))
                properties_tag.append(property_tag)

            instance_tag.append(properties_tag)

            for child_ref in instance.children_referents:
                child_instance = self.get_instance_from_referent(child_ref)
                instance_tag.append(instance_to_tag(child_instance))

            return instance_tag

        roblox_tag.append(instance_to_tag(self.root_instance))
        soup.append(roblox_tag)

        return soup
