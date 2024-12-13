from ..essentials import serialize, deserialize

VERSION = (1, 0, 0, 0)
BYTE_ORDER = "little"

_open = open    # naming duplicate f u 


def get_file(filename):
    with _open(filename, "rb") as f:
        return f.read()


def read_version(data):
    version = []
    buffer = bytearray()
    pointer = 0
    while len(version) < 4:
        if data[pointer] == 46:  # '.'
            version.append(int.from_bytes(buffer, BYTE_ORDER, signed=False))
            buffer.clear()
        else:
            buffer.append(data[pointer])
        pointer += 1

    return tuple(version), pointer


def get_all_flags(data):
    flags = []
    pointer = 0

    while data[pointer] != 0xFF and (len(data) > pointer + 1 or pointer < 256):
        flags.append(data[pointer])
        pointer += 1

    return flags, pointer


def open(data, password=None):
    version, offset = read_version(data)
    flags, offset2 = get_all_flags(data[offset:])

    if version > VERSION:
        print("Warning: File-Version is from the future. Expect bugs to occur.")

    raw_data = data[offset2 + offset + 1 :]

    for flag in reversed(flags):
        if flag == 0x01:
            if password is None:
                raise RuntimeError(
                    "This file is encrypted. Please pass a password on the argument."
                )
            from . import cryptography

            try:
                raw_data = cryptography.decrypt(raw_data, password)
            except (
                cryptography.InvalidToken
            ):  # ik im evil but i need a better error message
                raise RuntimeError("Could not decrypt file. Reason: Wrong password!")
        elif flag == 0x02:
            import zstandard

            raw_data = zstandard.decompress(raw_data)
        elif flag == 0x03:
            import lzma

            raw_data = lzma.decompress(raw_data)

    return deserialize(raw_data)


def open_file(filename, password=None):
    return open(get_file(filename), password)


def save(data, flags = None):
    if flags is None:
        flags = {}
    raw_data = serialize(data)

    flag_order = bytearray()

    for flag, options in flags.items():
        if flag == 0x01:
            from .cryptography import encrypt

            raw_data = encrypt(raw_data, options.get("password"))
        elif flag == 0x02:
            if options == False: continue
            from zstandard import compress

            raw_data = compress(raw_data)
        elif flag == 0x03:
            if options == False: continue
            from lzma import compress

            raw_data = compress(raw_data)
        else:
            raise NotImplementedError(f"This flag is not implemented/assigned. {flag}")
        flag_order.append(flag)

    data = (
        b".".join(
            [
                i.to_bytes((i.bit_length() // 8) + 1, "little", signed=False)
                for i in VERSION
            ]
        )
        + b"."
        + bytes(flag_order)
        + b"\xFF"
        + raw_data
    )

    return data


def save_file(filename, data, flags = None):
    raw_data = save(data, flags)
    with _open(filename, "wb") as f:
        f.write(raw_data)
