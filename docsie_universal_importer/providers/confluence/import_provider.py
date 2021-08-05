import json
import os
from dataclasses import dataclass
from pathlib import Path

import requests
from github import Github, ContentFile, Repository

from docsie_universal_importer.providers.base import (
    File, StorageViewer, StorageTree,
    Downloader, Provider, DownloaderAdapter,
    StorageViewerAdapter
)
from .serializers import GithubStorageTreeRequestSerializer, GithubDownloaderSerializer

class ConfluenceConnector:
    def __init__(self, email, token, site):
        self.site = site
        self.token = token
        self.email = email
        self.headers = {'Accept': 'application/json'}
        self.auth = (email, self.token)
        self.base_url = f"https://{self.site}.atlassian.net/wiki/rest/api/content"
    def _request(self, endpoint: str):
        if not endpoint[:1] == "/":  # adding slash pre endpoint if you forgot adding this
            endpoint = "/"+endpoint

        url = self.base_url + endpoint
        response = requests.get(url, auth=self.auth, headers=self.headers)

        return response
    def _get_page_html(self, page_id):
        response = self._request(endpoint=f"{page_id}?expand=body.storage").content
        return json.loads(response).get(
            "body", {}
        ).get(
            "storage", {}
        ).get(
            "value"
        )
    def _list_pages_ids(self):

        response = self._request("/").content  # request to the base url
        json_response = json.loads(response)
        ids = []
        for page in json_response.get("results",[]):
            ids.append(page.get("id"))
        return ids


@dataclass
class ConfluenceFile(File):
    id: str

    @classmethod
    def from_external(cls, file_obj: ContentFile, **kwargs):
        name = Path(file_obj.path).name

        return cls(name=name, path='')


class ConfluenceStorageViewer(StorageViewer):
    file_cls = ConfluenceFile

    def __init__(self, client: ConfluenceConnector):
        self.client = client

    def init_storage_tree(self) -> StorageTree:
        return StorageTree("")  # nothing

    def get_external_files(self):
        pages_ids = self.client._list_pages_ids()
        for page_id in pages_ids:
            file_obj = self.client._get_page_html(page_id)
            yield os.path.dirname(file_obj.path), file_obj


class ConfluenceDownloader(Downloader):
    file_cls = ConfluenceFile

    def __init__(self, client: ConfluenceConnector):
        self.client = client

    def download_file(self, file: ConfluenceFile):
        return self.client._get_page_html(file.id)


class ConfluenceDownloaderAdapter(DownloaderAdapter):
    adapted_cls = ConfluenceDownloader
    request_serializer_cls = GithubDownloaderSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']
        id = validated_data['id']
        email = validated_data['email']

        client = ConfluenceConnector(email=email, token=token, site="")  # TODO: make getting site!!!

        return {'page': client._get_page_html(page_id=id)}


class ConfluenceStorageViewerAdapter(StorageViewerAdapter):
    adapted_cls = ConfluenceStorageViewer
    request_serializer_cls = GithubStorageTreeRequestSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']
        id = validated_data['id']
        email = validated_data['email']

        client = ConfluenceConnector(email=email, token=token, site="")  # TODO: make getting site!!!

        return {'page': client._get_page_html(page_id=id)}


class GithubProvider(Provider):
    id = 'github'

    storage_viewer_adapter_cls = GithubStorageViewerAdapter
    downloader_adapter_cls = GithubDownloaderAdapter


provider_classes = [GithubProvider]
