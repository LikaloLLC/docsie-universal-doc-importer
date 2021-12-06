from docsie_universal_importer.providers.base import StorageTreeRequestSerializer, DownloaderRequestSerializer
from .file import GoogleDriveFile


class GoogleDriveStorageTreeRequestSerializer(StorageTreeRequestSerializer):
    pass


class GoogleDriveDownloaderSerializer(DownloaderRequestSerializer):
    class Meta:
        file_cls = GoogleDriveFile
