"""
SWJFF (Some weird Json File Format) Module [Python]. This module is used to serialize data.

Github: https://github.com/flamfrosticboio/SWJFF-Module-Python
"""

from typing import Union, Iterable, Mapping

JSONTypes = Union[
    int, float, str, bool, None, Mapping[str, "JSONTypes"], Iterable["JSONTypes"]
]

def serialize(data: JSONTypes) -> bytes:
    """Serializes data into a SWJFF format."""

def deserialize(data: bytes) -> JSONTypes:
    """Deserializes a SWJFF format."""
    
def open(data: bytes, password: str | None = None) -> JSONTypes:
    """Deserialize a sequence of bytes encoded in a file format."""
    
def open_file(filename: str, password: str | None = None) -> JSONTypes: 
    """Deserialize a file"""
    
def save(data: JSONTypes, flags: dict[int, dict | bool] = None) -> bytes: 
    """Serializes data into bytes for file storage."""
    
def save_file(filename: str, data: JSONTypes, flags: dict[int, dict | bool] = None) -> None:
    """Serializes data into file."""