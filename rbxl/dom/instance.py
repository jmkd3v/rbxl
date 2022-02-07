from typing import Dict, Optional, List

from ..types.referent import Referent


class Instance:
    def __init__(
            self,
            referent: Referent,
            class_name: str
    ):
        self.class_name = class_name
        self.referent: Referent = referent
        self._properties: Dict[str, bytes] = {}

        self.parent_referent: Optional[Referent] = None
        self.children_referents: List[Referent] = []

    def set_property(self, name: str, value: bytes):
        self._properties[name] = value

    def get_property(self, name: str):
        return self._properties[name]

    def get_properties(self):
        return self._properties.items()

    def __eq__(self, another):
        return hasattr(another, "referent") and another.referent == self.referent

    def __hash__(self):
        return hash(self.referent)

    def __repr__(self):
        return f"<{self.__class__.__name__} class_name={self.class_name} referent={self.referent.value}>"
