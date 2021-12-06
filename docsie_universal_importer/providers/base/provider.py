from abc import ABC, abstractmethod
from typing import Type

from django.utils.functional import cached_property

from docsie_universal_importer import app_settings
from docsie_universal_importer.import_adapter import ImportAdapter
from docsie_universal_importer.utils import required_class_attributes_checker, import_attribute
from .adapter import StorageViewerAdapter, DownloaderAdapter
from .downloader import Downloader


class SimpleProvider(ABC):
    """Simple provider class that downloads content and provides with a generic interface to get it."""
    id: str = None
    slug: str = None

    downloader_adapter_cls: Type[DownloaderAdapter] = None

    def __init__(self, request):
        required_class_attributes_checker(
            self.__class__, 'id', 'downloader_adapter_cls'
        )

        self.request = request

    @cached_property
    def downloader_adapter(self):
        return self.downloader_adapter_cls(self.request)

    @cached_property
    def downloader(self) -> Downloader:
        return self.downloader_adapter.get_adapted()

    def download_files(self):
        downloader = self.downloader

        for file_kwargs in self.downloader_adapter.get_files_data():
            file = self.downloader.get_file_from_kwargs(**file_kwargs)

            yield file, downloader.download_file(file)

    def get_import_adapter(self) -> ImportAdapter:
        settings = self.get_settings()
        path_to_adapter = settings.get('import_adapter') or app_settings.IMPORT_ADAPTER
        adapter = import_attribute(path_to_adapter)

        return adapter()

    def get_import_serializer(self):
        settings = self.get_settings()
        path_to_serializer = settings.get('import_serializer') or app_settings.IMPORT_SERIALIZER

        return import_attribute(path_to_serializer)

    @classmethod
    def get_settings(cls) -> dict:
        return app_settings.PROVIDERS.get(cls.id, {})

    @classmethod
    def get_package(cls):
        return getattr(cls, "package", None) or cls.__module__.rpartition(".")[0]

    @classmethod
    def get_slug(cls):
        return cls.slug or cls.id


class Provider(SimpleProvider):
    """Provider class that supports viewing files in a particular storage."""
    storage_viewer_adapter_cls: Type[StorageViewerAdapter] = None

    def __init__(self, request):
        required_class_attributes_checker('storage_viewer_adapter_cls')

        super().__init__(request)

    @abstractmethod
    def get_login_url(self):
        pass

    @cached_property
    def storage_viewer_adapter(self):
        return self.storage_viewer_adapter_cls(self.request)

    @cached_property
    def storage_viewer(self):
        return self.storage_viewer_adapter.get_adapted()

    def get_storage_tree(self) -> dict:
        storage_viewer = self.storage_viewer
        tree = storage_viewer.get_storage_tree()

        return tree.to_dict()
