from rbxl.binary.interleaving import deinterleave


def test_deinterleave():
    assert deinterleave(
        data=b"\xa0\xb0\xc0\xd0"
             b"\xa1\xb1\xc1\xd1"
             b"\xa2\xb2\xc2\xd2"
             b"\xa3\xb3\xc3\xd3",
        chunk_size=4
    ) == b"\xa0\xa1\xa2\xa3" \
         b"\xb0\xb1\xb2\xb3" \
         b"\xc0\xc1\xc2\xc3" \
         b"\xd0\xd1\xd2\xd3"

