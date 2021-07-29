from abc import ABC
from typing import Type

from django.utils.functional import cached_property

from docsie_universal_importer.app_settings import app_settings
from docsie_universal_importer.import_adapter import ImportAdapter
from docsie_universal_importer.utils import required_class_attributes_checker
from .adapter import StorageViewerAdapter, DownloaderAdapter
from .downloader import Downloader


class Provider(ABC):
    id: str = None

    storage_viewer_adapter_cls: Type[StorageViewerAdapter] = None
    downloader_adapter_cls: Type[DownloaderAdapter] = None

    def __init__(self, request):
        required_class_attributes_checker(
            self.__class__, 'id', 'storage_viewer_adapter_cls', 'downloader_adapter_cls'
        )

        self.request = request

    @cached_property
    def storage_viewer_adapter(self):
        return self.storage_viewer_adapter_cls(self.request)

    @cached_property
    def downloader_adapter(self):
        return self.downloader_adapter_cls(self.request)

    @cached_property
    def storage_viewer(self):
        return self.storage_viewer_adapter.get_adapted()

    @cached_property
    def downloader(self) -> Downloader:
        return self.downloader_adapter.get_adapted()

    def get_import_adapter(self) -> ImportAdapter:
        return app_settings.PROVIDERS[self.id].get('import_adapter') or app_settings.IMPORT_ADAPTER

    def get_storage_tree(self) -> dict:
        storage_viewer = self.storage_viewer
        tree = storage_viewer.get_storage_tree()

        return tree.to_dict()

    def download_files(self):
        downloader = self.downloader

        for file_kwargs in self.downloader_adapter.get_files_data():
            file = self.downloader.get_file_from_kwargs(**file_kwargs)

            yield file, downloader.download_file(file)

    @classmethod
    def get_package(cls):
        return getattr(cls, "package", None) or cls.__module__.rpartition(".")[0]
