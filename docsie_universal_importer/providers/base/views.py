from rest_framework.response import Response
from rest_framework.views import APIView

from docsie_universal_importer.providers import registry


def get_provider_cls(provider_id: str):
    return registry.by_id(provider_id)


class BaseView(APIView):
    @classmethod
    def provider_view(cls, provider):
        def view(request, *args, **kwargs):
            self = cls()
            self.request = request
            self.provider = provider(request)

            return self.dispatch(request, *args, **kwargs)

        return view


class StorageTreeView(BaseView):
    def get(self, request):
        return Response(self.provider.get_storage_tree())


class ImporterView(BaseView):
    def post(self, request):
        for file, content in self.provider.download_files():
            import_adapter = self.provider.get_import_adapter()
            import_adapter.import_file(file, content)

        return Response(status=200)
