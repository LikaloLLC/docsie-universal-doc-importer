from dataclasses import dataclass

from github import ContentFile

from docsie_universal_importer.providers.base import File


@dataclass
class ConfluenceFile(File):
    id: str

    @classmethod
    def from_external(cls, file_obj: ContentFile, **kwargs):
        name = file_obj.get('title')

        return cls(name=name, id=file_obj.get('id'))
