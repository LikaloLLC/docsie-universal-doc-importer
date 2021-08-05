from rest_framework import serializers

from docsie_universal_importer.providers.base import StorageTreeRequestSerializer, DownloaderRequestSerializer


class ConfluenceStorageTreeRequestSerializer(StorageTreeRequestSerializer):
    email = serializers.CharField()


class ConfluenceDownloaderSerializer(DownloaderRequestSerializer):
    email = serializers.CharField()
