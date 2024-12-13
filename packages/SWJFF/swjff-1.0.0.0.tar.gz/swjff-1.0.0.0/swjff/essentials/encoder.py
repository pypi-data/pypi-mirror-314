# [Encoder] by flamfrostboio

# * this encoder is still not optimized
# * its just my implementation to show the idea of it
# ! this is not for production use

from collections.abc import Iterable, Mapping
import struct

BYTE_ORDER = "little"
SPECIAL_CHARACTERS = {0xFA, 0xFB, 0xFC, 0xFD, 0xFE, 0xFF}

intToByte = lambda value: value.to_bytes(1, BYTE_ORDER, signed=False)
write = lambda type, data: chr(type).encode() + data


# code is untested for other cases
def serialize_int(d: int):
    bl = d.bit_length()

    for i, bit in enumerate([8, 16, 32, 64, 128]):
        if bl > bit:
            continue
        if d >= 0:
            return write(2 + (i * 2), d.to_bytes((bit + 7) // 8, BYTE_ORDER))
        if d >= -(2**bit) / 2:
            return write(
                1 + (i * 2), d.to_bytes((bit + 7) // 8, BYTE_ORDER, signed=True)
            )
    raise ValueError("integer value is too large to be serialized.")


# i hate this method
def float_range(value):
    try:
        half_precision = struct.unpack("e", struct.pack("e", value))[0]
        if half_precision == value:
            return 3
    except Exception:
        pass
    single_precision = struct.unpack("f", struct.pack("f", value))[0]
    if single_precision == value:
        return 1
    return 2


def serialize_float(f: float):
    result = float_range(f)
    if result == 1:
        return write(13, struct.pack("f", f))
    elif result == 2:
        return write(14, struct.pack("d", f))
    elif result == 3:
        return write(15, struct.pack("e", f))


# some weird technique
def serialize_char(c: str):
    ref = c.encode("utf-8")
    if len(ref) == 1:
        return write(11, ord(ref).to_bytes(1, BYTE_ORDER, signed=False))
    return write(12, c.encode("utf-32"))


def serialize_bool(b: bool):
    return write(20 if b == True else 21, b"")


def serialize_array(a):
    is_special_allowed, group_type = one_type_array_allowed(a)
    if is_special_allowed:
        return write(30, intToByte(group_type) + b"".join([serialize(item)[1:2] for item in a]) + b"\xFA")
    return write(23, b"".join([serialize(item) for item in a]) + b"\xFA")


def serialize_mapping(m):
    return write(
        24,
        b"".join([serialize(key) + serialize(value) for key, value in m.items()])
        + b"\xFB",
    )


def prepare_data(data: bytes):
    new_data = bytearray()
    for i in range(len(data)):
        if data[i] in SPECIAL_CHARACTERS:
            new_data.append(0xFD)
        new_data.append(data[i])
    return new_data


def serialize(data):
    if isinstance(data, bool):
        return serialize_bool(data)
    elif isinstance(data, int):
        return serialize_int(data)
    elif isinstance(data, float):
        return serialize_float(data)
    elif isinstance(data, str):
        if len(data) == 0:
            return write(18, b"\xff")
        if len(data) == 1:
            return serialize_char(data)
        return write(18, data.encode("utf-8") + b"\xff")
    elif isinstance(data, bytes):
        data = prepare_data(data)
        return write(19, data + b"\xff")
    elif data is None:
        return write(22, b"")
    elif isinstance(data, Mapping):
        return serialize_mapping(data)
    elif isinstance(data, Iterable):
        return serialize_array(data)


def one_type_array_allowed(array: list):
    type = None
    for item in array:
        if type == None:
            type = serialize(item)[0]
            continue
        if type != serialize(item)[0]:
            return False, None
    return True, type
