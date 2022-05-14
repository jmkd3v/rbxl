from base64 import b64decode
from dataclasses import dataclass
from typing import Dict, Callable, Any, Optional, Tuple

from bs4.element import Tag

from ..types.referent import Referent


@dataclass
class CFrame:
    x: float
    y: float
    z: float
    r00: float
    r01: float
    r02: float
    r10: float
    r11: float
    r12: float
    r20: float
    r21: float
    r22: float


@dataclass
class Vector3:
    x: float
    y: float
    z: float


@dataclass
class Color3:
    r: float
    g: float
    b: float


def bool_handler(tag: Tag) -> bool:
    return tag.get_text().strip().lower() == "true"


def float_double_handler(tag: Tag) -> float:
    return float(tag.get_text().strip())


def int_handler(tag: Tag) -> int:
    return int(tag.get_text().strip())


def cframe_handler(tag: Tag) -> CFrame:
    return CFrame(
        x=float(tag.find("X").get_text().strip()),
        y=float(tag.find("Y").get_text().strip()),
        z=float(tag.find("Z").get_text().strip()),

        r00=float(tag.find("R00").get_text().strip()),
        r01=float(tag.find("R01").get_text().strip()),
        r02=float(tag.find("R02").get_text().strip()),

        r10=float(tag.find("R10").get_text().strip()),
        r11=float(tag.find("R11").get_text().strip()),
        r12=float(tag.find("R12").get_text().strip()),

        r20=float(tag.find("R20").get_text().strip()),
        r21=float(tag.find("R21").get_text().strip()),
        r22=float(tag.find("R22").get_text().strip())
    )


def optional_cframe_handler(tag: Tag) -> Optional[CFrame]:
    cframe_tag = tag.find("CFrame", recursive=False)
    if cframe_tag:
        return cframe_handler(cframe_tag)
    else:
        return None


def vector3_handler(tag: Tag) -> Vector3:
    return Vector3(
        x=float(tag.find("X").get_text().strip()),
        y=float(tag.find("Y").get_text().strip()),
        z=float(tag.find("Z").get_text().strip()),
    )


def string_handler(tag: Tag) -> str:
    return tag.get_text()


def referent_handler(tag: Tag) -> Optional[Referent]:
    raw_text = tag.get_text().strip()
    if raw_text == "null":
        return None
    else:
        return Referent.from_hex(raw_text[3:])


def token_handler(tag: Tag) -> int:
    return int(tag.get_text().strip())


def binary_string_handler(tag: Tag) -> bytes:
    return b64decode(tag.get_text().strip())


def unique_id_handler(tag: Tag) -> int:
    return int(tag.get_text().strip(), base=16)


def color3_handler(tag: Tag) -> Color3:
    return Color3(
        r=float(tag.find("R").get_text().strip()),
        g=float(tag.find("G").get_text().strip()),
        b=float(tag.find("B").get_text().strip()),
    )


def color3uint8_handler(tag: Tag) -> Color3:
    int8 = int(tag.get_text().strip())
    return Color3(
        r=((int8 >> 16) & 0xFF) / 0xFF,
        g=((int8 >> 8) & 0xFF) / 0xFF,
        b=((int8 & 0xFF) / 0xFF)
    )


_element_name_to_handlers: Dict[str, Tuple[Callable[[Tag], Any], Callable[[Tag], Any]]] = {
    "string": (None, string_handler),
    "bool": (None, bool_handler),
    "float": (None, float_double_handler),
    "double": (None, float_double_handler),
    "int64": (None, int_handler),
    "int": (None, int_handler),
    "CoordinateFrame": (None, cframe_handler),
    "OptionalCoordinateFrame": (None, optional_cframe_handler),
    "Vector3": (None, vector3_handler),
    "Ref": (None, referent_handler),
    "token": (None, token_handler),
    "BinaryString": (None, binary_string_handler),
    "UniqueId": (None, unique_id_handler),
    "Color3": (None, color3_handler),
    "Color3uint8": (None, color3uint8_handler)
}


def get_encoder_for_type(type_name: str) -> Callable[[Tag], Any]:
    return _element_name_to_handlers[type_name][1]


def get_decoder_for_type(type_name: str) -> Callable[[Tag], Any]:
    return _element_name_to_handlers[type_name][0]
