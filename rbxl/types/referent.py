from __future__ import annotations


class Referent:
    """
    A Referent is a unique identifier that references a Roblox instance.
    """

    def __init__(self, data: int):
        self.data: int = data

    @classmethod
    def from_hex(cls, hex_data: str) -> Referent:
        """
        Builds a new Referent from a hexadecimal string.

        Arguments:
            hex_data: The hexadecimal string.
        """
        return cls(int(
            hex_data,
            base=16
        ))

    def to_hex(self) -> str:
        """
        Returns the Referent interpreted as hexadecimal data.
        """
        return f"{self.data:032x}"
