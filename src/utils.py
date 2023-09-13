from dataclasses import dataclass
from typing import Optional


@dataclass
class FileData:
    filename: str
    extension: Optional[str]
    size_in_bytes: int
    path: str
