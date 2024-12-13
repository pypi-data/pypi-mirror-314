"""A SWJFF converting module. Essentials Only"""

from typing import Union, Iterable, Mapping

JSONTypes = Union[
    int, float, str, bool, None, Mapping[str, "JSONTypes"], Iterable["JSONTypes"]
]

def serialize(data: JSONTypes) -> bytes:
    """Serializes data into a SWJFF format."""

def deserialize(data: bytes) -> JSONTypes:
    """Deserializes a SWJFF format."""
