from dataclasses import dataclass
from pathlib import Path

import github
from github import Github, ContentFile, Repository

from docsie_universal_importer.providers.base import (
    File, StorageViewer, StorageTree,
    Downloader, Provider, DownloaderAdapter,
    StorageViewerAdapter
)
from .serializers import GithubStorageTreeRequestSerializer, GithubDownloaderSerializer


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
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(self.repo.get_contents(file_content.path))
            else:
                yield file_content.path, file_content.path


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

    def unauthorized_error(self):
        return github.BadCredentialsException

    def forbidden_error(self):
        return github.BadCredentialsException

    def not_found_error(self):
        return github.UnknownObjectException

    def bad_request_error(self):
        return None


provider_classes = [GithubProvider]
