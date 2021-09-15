from docsie_universal_importer.providers.base import StorageTreeRequestSerializer, DownloaderRequestSerializer
from .file import BoxFile


class BoxStorageTreeRequestSerializer(StorageTreeRequestSerializer):
    pass


class BoxDownloaderSerializer(DownloaderRequestSerializer):
    class Meta:
        file_cls = BoxFile
