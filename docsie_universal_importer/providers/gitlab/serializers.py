from rest_framework import serializers

from docsie_universal_importer.providers.base import StorageTreeRequestSerializer, DownloaderRequestSerializer
from .file import GitlabFile


class GitlabStorageTreeRequestSerializer(StorageTreeRequestSerializer):
    repo = serializers.CharField()


class GitlabDownloaderSerializer(DownloaderRequestSerializer):
    repo = serializers.CharField()

    class Meta:
        file_cls = GitlabFile
