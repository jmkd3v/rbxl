from rbxl.types.referent import Referent


def test_from_hex():
    assert Referent.from_hex("00000000000000000000000000000000").data == 0
    assert Referent.from_hex("00000000300000e00f00000000000001").data == 14855284604576099720297971713
    assert Referent.from_hex("ffffffffffffffffffffffffffffffff").data == 340282366920938463463374607431768211455


def test_to_hex():
    assert Referent(0).to_hex() == "00000000000000000000000000000000"
    assert Referent(14855284604576099720297971713).to_hex() == "00000000300000e00f00000000000001"
    assert Referent(340282366920938463463374607431768211455).to_hex() == "ffffffffffffffffffffffffffffffff"
