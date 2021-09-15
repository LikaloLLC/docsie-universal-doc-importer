import os

from google.cloud.storage import Client
from google.oauth2.credentials import Credentials

from docsie_universal_importer.providers.base import (
    StorageViewer, StorageTree,
    Downloader, DownloaderAdapter,
    StorageViewerAdapter
)
from .file import GoogleCloudStorageFile
from .serializers import GoogleCloudStorageTreeRequestSerializer, GoogleCloudStorageDownloaderSerializer
from ..oauth2.provider import OAuth2Provider


class GoogleCloudStorage(Client):
    def __init__(self, token):
        credentials = Credentials(token=token)

        super().__init__(credentials=credentials)


class GoogleCloudStorageViewer(StorageViewer):
    file_cls = GoogleCloudStorageFile

    def __init__(self, bucket):
        self.bucket = bucket

    def init_storage_tree(self) -> StorageTree:
        return StorageTree(self.bucket.name)

    def get_external_files(self):
        blobs = self.bucket.list_blobs()

        for blob in blobs:
            yield os.path.dirname(blob.name.strip('/')), blob


class GoogleCloudStorageDownloader(Downloader):
    file_cls = GoogleCloudStorageFile

    def __init__(self, bucket):
        self.bucket = bucket

    def download_file(self, file: GoogleCloudStorageFile):
        blob = self.bucket.blob(file.path)

        return blob.download_as_string()


class GoogleCloudStorageDownloaderAdapter(DownloaderAdapter):
    adapted_cls = GoogleCloudStorageDownloader
    request_serializer_cls = GoogleCloudStorageDownloaderSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']
        bucket = validated_data['bucket']

        client = GoogleCloudStorage(token)

        return {'bucket': client.get_bucket(bucket)}


class GoogleCloudStorageViewerAdapter(StorageViewerAdapter):
    adapted_cls = GoogleCloudStorageViewer
    request_serializer_cls = GoogleCloudStorageTreeRequestSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']
        bucket = validated_data['bucket']

        client = GoogleCloudStorage(token)

        return {'bucket': client.get_bucket(bucket)}


class GoogleCloudStorageOAuth2Provider(OAuth2Provider):
    id = 'google_cloud_storage'

    storage_viewer_adapter_cls = GoogleCloudStorageViewerAdapter
    downloader_adapter_cls = GoogleCloudStorageDownloaderAdapter


provider_classes = [GoogleCloudStorageOAuth2Provider]
