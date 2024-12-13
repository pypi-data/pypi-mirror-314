from struct import unpack

CURRENT_VERSION = (1, 0, 0, 0)
BYTE_ORDER = "little"
SPECIAL_CHARACTERS = {0xFA, 0xFB, 0xFC, 0xFD, 0xFE, 0xFF}


def get_until(data, start=1, terminator=0xFF):
    buffer = bytearray()
    ignored_counter = 0
    ignore = False

    while start < len(data):
        if ignore:
            ignore = False
            buffer.append(data[start])
        elif data[start] == 0xFD:
            ignore = True
            ignored_counter += 1
        elif data[start] == terminator:
            break
        else:
            buffer.append(data[start])

        start += 1

    return bytes(buffer), ignored_counter


def read_array(data: bytes):
    buffer = []
    pointer = 1

    while pointer < len(data):
        if data[pointer] == 0xFA:
            break

        result, mov = deserialize_item(data[pointer:])
        buffer.append(result)
        pointer += mov + 1
    return buffer, pointer


def read_mapping(data: bytes):
    pointer = 1
    buffer = {}
    while pointer < len(data):
        if data[pointer] == 0xFB:
            break

        key, key_mov = deserialize_item(data[pointer:])
        pointer += key_mov + 1

        value, value_mov = deserialize_item(data[pointer:])
        pointer += value_mov + 1

        buffer[key] = value
    return buffer, pointer

def read_special_array(data):
    buffer = []
    pointer = 2
    type = data[1:2]

    while pointer < len(data):
        if data[pointer] == 0xFA:
            break
        result, mov = deserialize_item(type + data[pointer:pointer+1])
        pointer += mov
        buffer.append(result)
    return buffer, pointer


def deserialize_item(data: bytes):
    if data[0] == 0x01:
        return int.from_bytes(data[1:2], BYTE_ORDER, signed=True), 1
    elif data[0] == 2:
        return int.from_bytes(data[1:2], BYTE_ORDER, signed=False), 1
    elif data[0] == 3:
        return int.from_bytes(data[1:3], BYTE_ORDER, signed=True), 2
    elif data[0] == 4:
        return int.from_bytes(data[1:3], BYTE_ORDER, signed=False), 2
    elif data[0] == 5:
        return int.from_bytes(data[1:5], BYTE_ORDER, signed=True), 4
    elif data[0] == 6:
        return int.from_bytes(data[1:5], BYTE_ORDER, signed=False), 4
    elif data[0] == 7:
        return int.from_bytes(data[1:9], BYTE_ORDER, signed=True), 8
    elif data[0] == 8:
        return int.from_bytes(data[1:9], BYTE_ORDER, signed=False), 8
    elif data[0] == 9:
           return int.from_bytes(data[1:17], BYTE_ORDER, signed=True), 16
    elif data[0] == 10:
        return int.from_bytes(data[1:17], BYTE_ORDER, signed=False), 16
    elif data[0] == 11:
        return data[1:2].decode("utf-8"), 1
    elif data[0] == 12:
        return data[1:9].decode("utf-32"), 8
    elif data[0] == 13:
        return unpack("f", data[1:5])[0], 4
    elif data[0] == 14:
        return unpack("d", data[1:9])[0], 8
    elif data[0] == 15:
        return unpack("e", data[1:3])[0], 2
    elif data[0] == 18:
        sanitized, ignored = get_until(data)
        decoded = sanitized.decode("utf-8")
        return decoded, len(sanitized) + ignored + 1
    elif data[0] == 19:
        decoded, ignored = get_until(data)
        return decoded, len(decoded) + ignored + 1
    elif data[0] == 20:
        return True, 0
    elif data[0] == 21:
        return False, 0
    elif data[0] == 22:
        return None, 0
    elif data[0] == 23:
        return read_array(data)
    elif data[0] == 24:
        return read_mapping(data)
    elif data[0] == 30:
        return read_special_array(data)
    else:
        raise ValueError(f"Invalid type: {data[0:1]} -> {data[0]}")


def deserialize(data: bytes):
    return deserialize_item(data)[0]