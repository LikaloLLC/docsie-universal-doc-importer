from docsie_universal_importer.providers.base import StorageTreeRequestSerializer, DownloaderRequestSerializer
from .files import GoogleDriveFile


class GoogleDriveStorageTreeRequestSerializer(StorageTreeRequestSerializer):
    pass


class GoogleDriveDownloaderSerializer(DownloaderRequestSerializer):
    class Meta:
        file_cls = GoogleDriveFile
