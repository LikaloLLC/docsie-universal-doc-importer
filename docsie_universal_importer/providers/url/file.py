from dataclasses import dataclass

from docsie_universal_importer.providers.base import File


@dataclass
class URLFile(File):
    url: str

    @classmethod
    def from_external(cls, file_obj, **kwargs):
        url = file_obj['url']
        name = url.split('/')[-1]

        return cls(name=name, url=url)
