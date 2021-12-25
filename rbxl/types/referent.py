from __future__ import annotations
from typing import List


class Referent:
    """
    A Referent is a unique identifier that references a Roblox instance.
    """

    def __init__(self, value: int):
        self.value: int = value

    @classmethod
    def from_hex(cls, hex_data: str) -> Referent:
        """
        Builds a new Referent from a hexadecimal string.
        The passed string should be equal to the result of the `to_hex` method when run on the new Referent.

        Arguments:
            hex_data: The hexadecimal string.

        Returns:
            A new Referent.
        """
        return cls(int(
            hex_data,
            base=16
        ))

    def to_hex(self) -> str:
        """
        Converts the Referent to hexadecimal data.
        This data can be passed to `from_hex` to get an identical referent.

        Returns:
            A hexadecimal string of length 32.
        """
        return f"{self.value:032x}"

    @classmethod
    def from_bytes(cls, bytes_data: bytes) -> Referent:
        """
        Builds a new Referent from bytes.

        Arguments:
            bytes_data: The bytes.

        Returns:
            A new Referent.
        """
        return cls(int.from_bytes(
            bytes=bytes_data,
            byteorder="big",
            signed=True
        ))

    def to_bytes(self) -> bytes:
        """
        Converts the Referent to bytes.

        Returns:
            The Referent as bytes.
        """
        return self.value.to_bytes(
            length=16,
            byteorder="big",
            signed=True
        )

    @classmethod
    def from_ints_accumulated(cls, ints_list: List[int]) -> List[Referent]:
        """
        Gets multiple Referents from a list of accumulated Referent bytes.
        """
        referents: List[Referent] = [Referent(ints_list[0])]

        for int_data in ints_list[1:]:
            referents.append(Referent(int_data + referents[len(referents) - 1].value))

        return referents

    def __eq__(self, another):
        return hasattr(another, "value") and another.value == self.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return f"<{self.__class__.__name__} value={self.value}>"
