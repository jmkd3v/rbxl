from typing import Optional, Dict


class Instance:
    def __init__(
            self,
            referent: Referent,
            class_name: str
    ):
        self.class_name = class_name
        self.properties: Dict[str, Variant] = {}
    