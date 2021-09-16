from dataclasses import dataclass
from pathlib import Path

from docsie_universal_importer.providers.base import File


@dataclass
class GoogleDriveFile(File):
    id: str

    @classmethod
    def from_external(cls, file_obj, **kwargs):
        name = Path(file_obj['name']).name

        return cls(name=name, id=file_obj['id'])
