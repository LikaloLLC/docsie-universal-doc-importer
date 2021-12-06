from rest_framework import serializers

from .file import URLFile
from ..base.serializers import SimpleDownloaderRequestSerializer


class URLDownloaderSerializer(SimpleDownloaderRequestSerializer):
    login = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    class Meta:
        file_cls = URLFile
