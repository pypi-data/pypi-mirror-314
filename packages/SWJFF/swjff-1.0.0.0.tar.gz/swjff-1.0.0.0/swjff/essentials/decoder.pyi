"""The decoder module for deserializing SWJFF format"""

from typing import Union, Iterable, Mapping

JSONTypes = Union[
    int, float, str, bool, None, Mapping[str, "JSONTypes"], Iterable["JSONTypes"]
]

def deserialize(data: bytes) -> JSONTypes:
    """Deserializes a SWJFF format."""
