from typing import Optional, Dict
from .instance import Instance


class RobloxDOM:
    def __init__(self):
        self.referents = []
        self.root_instance: Optional[Instance] = None
        self._referent_to_instance: Dict[str, Instance] = {}
