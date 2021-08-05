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
class GithubFile(File):
    path: str

    @classmethod
    def from_external(cls, file_obj: ContentFile, **kwargs):
        name = Path(file_obj.path).name

        return cls(name=name, path=file_obj.path)


class GithubStorageViewer(StorageViewer):
    file_cls = GithubFile

    def __init__(self, repo: Repository):
        self.repo = repo

    def init_storage_tree(self) -> StorageTree:
        return StorageTree(self.repo.full_name)

    def get_external_files(self):
        contents = self.repo.get_contents("")
        while contents:
            file_obj = contents.pop(0)
            if file_obj.type == "dir":
                contents.extend(self.repo.get_contents(file_obj.path))
            else:
                yield os.path.dirname(file_obj.path), file_obj


class GithubDownloader(Downloader):
    file_cls = GithubFile

    def __init__(self, repo: Repository):
        self.repo = repo

    def download_file(self, file: GithubFile):
        return self.repo.get_contents(file.path).decoded_content.decode()


class GithubDownloaderAdapter(DownloaderAdapter):
    adapted_cls = GithubDownloader
    request_serializer_cls = GithubDownloaderSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']
        repo_name = validated_data['repo']

        client = Github(token)

        return {'repo': client.get_repo(full_name_or_id=repo_name)}


class GithubStorageViewerAdapter(StorageViewerAdapter):
    adapted_cls = GithubStorageViewer
    request_serializer_cls = GithubStorageTreeRequestSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']
        repo_name = validated_data['repo']

        client = Github(token)

        return {'repo': client.get_repo(full_name_or_id=repo_name)}


class GithubProvider(Provider):
    id = 'github'

    storage_viewer_adapter_cls = GithubStorageViewerAdapter
    downloader_adapter_cls = GithubDownloaderAdapter


provider_classes = [GithubProvider]
