from dataclasses import dataclass
from typing import Optional


class InvalidQueryException(Exception):
    ...


@dataclass
class FileData:
    filename: str
    extension: Optional[str]
    size_in_bytes: int
    path: str

    @staticmethod
    def from_index(data: dict):
        return FileData(filename=data['filename'],
                        extension=data.get('extension'),
                        size_in_bytes=data['size'],
                        path=data['path'])
