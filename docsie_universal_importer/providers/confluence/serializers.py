from docsie_universal_importer.providers.base import StorageTreeRequestSerializer, DownloaderRequestSerializer
from .file import ConfluenceFile


class ConfluenceStorageTreeRequestSerializer(StorageTreeRequestSerializer):
    pass


class ConfluenceDownloaderSerializer(DownloaderRequestSerializer):
    class Meta:
        file_cls = ConfluenceFile
