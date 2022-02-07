from typing import Dict, Callable, Any, Optional

from dataclasses import dataclass
from bs4.element import Tag
from base64 import b64decode

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


element_name_to_handler: Dict[str, Callable[[Tag], Any]] = {
    "string": string_handler,
    "bool": bool_handler,
    "float": float_double_handler,
    "double": float_double_handler,
    "int64": int_handler,
    "int": int_handler,
    "CoordinateFrame": cframe_handler,
    "Vector3": vector3_handler,
    "Ref": referent_handler,
    "token": token_handler,
    "BinaryString": binary_string_handler,
    "UniqueId": unique_id_handler
}
