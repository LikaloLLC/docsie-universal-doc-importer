from dataclasses import dataclass
from pathlib import Path

from docsie_universal_importer.providers.base import File


@dataclass
class GitlabFile(File):
    path: str

    @classmethod
    def from_external(cls, file_obj, **kwargs):
        name = Path(file_obj['path']).name

        return cls(name=name, path=file_obj['path'])

