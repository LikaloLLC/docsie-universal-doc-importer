from dataclasses import dataclass
from pathlib import Path

from github.ContentFile import ContentFile

from ..base import File


@dataclass
class GithubFile(File):
    path: str

    @classmethod
    def from_external(cls, file_obj: ContentFile, **kwargs):
        name = Path(file_obj.path).name

        return cls(name=name, path=file_obj.path)
