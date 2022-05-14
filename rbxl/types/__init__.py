from enum import IntEnum


class DataType(IntEnum):
    string = 0x01
    bool = 0x02
    int32 = 0x03
    float32 = 0x04
    float64 = 0x05
    udim = 0x06
    udim2 = 0x07
    ray = 0x08
    faces = 0x09
    axes = 0x0a
    brickcolor = 0x0b
    color3 = 0x0c
    vector2 = 0x0d
    vector3 = 0x0e
    cframe = 0x10
    enum = 0x12
    referent = 0x13
    vector3int16 = 0x14
    numbersequence = 0x15
    colorsequence = 0x16
    numberrange = 0x17
    rect = 0x18
    physicalproperties = 0x19
    color3uint8 = 0x1a
    int64 = 0x1b
    sharedstring = 0x1c
    bytecode = 0x1d
    optionalcoordinateframe = 0x1e
    uniqueid = 0x1f
