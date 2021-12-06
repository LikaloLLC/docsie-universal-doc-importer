import requests

from docsie_universal_importer.providers.base import (
    Downloader, DownloaderAdapter,
)
from .file import URLFile
from .serializers import URLDownloaderSerializer
from ..base.provider import SimpleProvider


class URLDownloader(Downloader):
    file_cls = URLFile

    def __init__(self, login=None, password=None):
        self.auth = None
        if login and password:
            self.auth = (login, password)

    def download_file(self, file: URLFile):
        return requests.get(file.url, auth=self.auth).content


class URLDownloaderAdapter(DownloaderAdapter):
    adapted_cls = URLDownloader
    request_serializer_cls = URLDownloaderSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        return {'login': validated_data.get('login'), 'password': validated_data.get('password')}


class URLOAuth2Provider(SimpleProvider):
    id = 'html'

    downloader_adapter_cls = URLDownloaderAdapter


provider_classes = [URLOAuth2Provider]
