from rest_framework import serializers

from docsie_universal_importer.providers.base import StorageTreeRequestSerializer, DownloaderRequestSerializer
from .file import GoogleCloudStorageFile


class GoogleCloudStorageTreeRequestSerializer(StorageTreeRequestSerializer):
    bucket = serializers.CharField()


class GoogleCloudStorageDownloaderSerializer(DownloaderRequestSerializer):
    bucket = serializers.CharField()

    class Meta:
        file_cls = GoogleCloudStorageFile
