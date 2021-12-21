from .file import BinaryFile, FileType


def from_bytes(data: bytes, file_type: FileType):
    if file_type == FileType.binary:
        return BinaryFile(data)
    else:
        return BinaryFile(data)
