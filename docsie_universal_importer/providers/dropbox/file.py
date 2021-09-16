from dataclasses import dataclass

from docsie_universal_importer.providers.base import File


@dataclass
class DropboxFile(File):
    path: str

    @classmethod
    def from_external(cls, file_obj, **kwargs):
        return cls(name=file_obj.name, path=file_obj.path_lower)
