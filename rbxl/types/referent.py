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
        return f"{self.data:032x}"

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
            signed=False
        ))

    def to_bytes(self) -> bytes:
        """
        Converts the Referent to bytes.

        Returns:
            The Referent as bytes.
        """
        return self.data.to_bytes(
            length=16,
            byteorder="big",
            signed=False
        )
