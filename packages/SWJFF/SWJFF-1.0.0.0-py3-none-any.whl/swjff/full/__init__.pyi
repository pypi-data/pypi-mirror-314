"""An extended modules for SWJFF.

Included in this package:
- File Format
- Command Line Interface
"""

from ..essentials.encoder import JSONTypes

def open(data: bytes, password: str | None = None) -> JSONTypes:
    """Deserialize a sequence of bytes encoded in a file format."""
    
def open_file(filename: str, password: str | None = None) -> JSONTypes: 
    """Deserialize a file"""
    
def save(data: JSONTypes, flags: dict[int, dict | bool] = None) -> bytes: 
    """Serializes data into bytes for file storage."""
    
def save_file(filename: str, data: JSONTypes, flags: dict[int, dict | bool] = None) -> None:
    """Serializes data into file."""