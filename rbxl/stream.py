from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Optional, Literal


def deinterleave(data, chunk_size):
    """
    Deinterleaves interleaved bytes.
    """
    chunk_count = len(data) // chunk_size
    return bytes([
        data[j * chunk_count + i] for i in range(chunk_count) for j in range(chunk_size)
    ])


def transform_int(value: int):
    return (value << 1) ^ (value >> 31)


def untransform_int(value: int):
    return (value >> 1) ^ -(value & 1)


class RbxStream:
    def __init__(
            self,
            *,
            stream: BinaryIO,
            enforce_eof: bool = True
    ):
        self.stream = stream
        self.enforce_eof: bool = enforce_eof

    # Reading
    def read(self, length: Optional[int] = None) -> bytes:
        if length is None:
            return self.stream.read()
        else:
            if self.enforce_eof:
                offset = self.stream.tell()
                data = self.stream.read(length)
                if len(data) < length:
                    self.stream.seek(offset)
                    raise EOFError("end of file reached")
                return data
            else:
                return self.stream.read(length)

    def read_n(self) -> bytes:
        length = self.read_int(length=4)
        return self.read(length)

    def read_interleaved(self, length: int, count: int) -> bytes:
        return deinterleave(self.read(length * count), length)

    def read_string(self, length: int, encoding: str = "ascii") -> str:
        return self.read(length).decode(encoding)

    def read_n_string(self, encoding: str = "ascii") -> str:
        """
        Reads an unsigned 4-byte integer and passes it as length to read_string.
        """
        return self.read_n().decode(encoding)

    def read_int(
            self,
            length: int,
            byteorder: Literal["little", "big"] = "little",
            signed: bool = False,
            transform: bool = False
    ) -> int:
        value = int.from_bytes(
            bytes=self.read(length),
            byteorder=byteorder,
            signed=signed
        )

        if transform:
            return untransform_int(value)
        else:
            return value

    def read_interleaved_ints(
            self,
            length: int,
            count: int,
            byteorder: Literal["little", "big"],
            signed: bool = False,
            transform: bool = False
    ) -> list[int]:
        data = self.read_interleaved(length, count)

        if transform:
            return [
                untransform_int(int.from_bytes(
                    bytes=data[i:i+4],
                    byteorder=byteorder,
                    signed=signed
                )) for i in range(0, len(data), 4)
            ]
        else:
            return [
                int.from_bytes(
                    bytes=data[i:i+4],
                    byteorder=byteorder,
                    signed=signed
                ) for i in range(0, len(data), 4)
            ]

    def read_bool(self) -> bool:
        data = self.read(1)
        if data == b"\x00":
            return False
        elif data == b"\x01":
            return True
        else:
            self.seek(self.tell() - 1)
            raise ValueError(f"cannot interpret byte as bool: {data}")

    # Writing
    def write(self, data: bytes) -> int:
        return self.stream.write(data)

    def write_n(self, data: bytes) -> int:
        return self.write_int(
            data=len(data),
            length=4
        ) + self.write(data)

    def write_string(self, data: str, encoding: str = "ascii") -> int:
        return self.write(data.encode(encoding))

    def write_n_string(self, data: str, encoding: str = "ascii"):
        return self.write_n(data.encode(encoding))

    def write_int(
            self,
            data: int,
            length: int,
            *,
            byteorder: Literal["little", "big"] = "little",
            signed: bool = False
    ) -> int:
        return self.write(
            int.to_bytes(self=data, length=length, byteorder=byteorder, signed=signed)
        )

    def write_bool(self, data: bool) -> int:
        if data:
            return self.write(b"\x01")
        else:
            return self.write(b"\x00")

    # Misc
    def seek(self, offset: int, whence: int = 0):
        return self.stream.seek(offset, whence)

    def tell(self):
        return self.stream.tell()

    def skip(self, offset: int):
        return self.seek(offset, 1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.stream.__exit__(exc_type, exc_val, exc_tb)

    def __repr__(self):
        return f"<{self.__class__.__name__} name={self.stream.name!r}>"


def rbx_open(path: str | Path, mode: Literal["r", "w"]) -> RbxStream:
    if mode == "r":
        real_mode = "rb"
    elif mode == "w":
        real_mode = "wb"
    else:
        raise ValueError("invalid mode")

    return RbxStream(
        stream=open(  # type: ignore
            file=path,
            mode=real_mode
        )
    )


if __name__ == '__main__':
    ...
