from docsie_universal_importer.providers.base import StorageTreeRequestSerializer, DownloaderRequestSerializer
from .file import DropboxFile


class DropboxStorageTreeRequestSerializer(StorageTreeRequestSerializer):
    pass


class DropboxDownloaderSerializer(DownloaderRequestSerializer):
    class Meta:
        file_cls = DropboxFile
