class Referent:
    def __init__(self, data: int):
        self.data: int = data

    @classmethod
    def from_hex(cls, hex_data: str):
        return cls(int(
            hex_data,
            base=16
        ))

    def to_hex(self) -> str:
        return f"{self.data:032x}"
