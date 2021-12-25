from typing import Literal

def untransform_int(value: int):
    return (value >> 1) ^ -(value & 1)


def deinterleave(data, chunk_size):
    """
    Deinterleaves interleaved bytes.
    """
    chunk_count = len(data) // chunk_size
    data = bytes([data[j * chunk_count + i] for i in range(chunk_count) for j in range(chunk_size)])
    return data


def deinterleave_int(
        data,
        byte_order: Literal["little", "big"] = "big",
        signed=False,
        untransform=True
):
    """
    Deinterleaves interleaved int32s.
    """
    deinterleaved_data = deinterleave(
        data=data,
        chunk_size=4
    )
    ints = []

    for int_index in range(0, len(deinterleaved_data), 4):
        int_data = deinterleaved_data[int_index:int_index + 4]
        chunk_int = int.from_bytes(
            bytes=int_data,
            byteorder=byte_order,
            signed=signed
        )
        if untransform:
            ints.append(untransform_int(chunk_int))
        else:
            ints.append(chunk_int)

    return ints
