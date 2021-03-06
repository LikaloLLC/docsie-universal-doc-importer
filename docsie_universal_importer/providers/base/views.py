import json

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from docsie_universal_importer.models import ConnectorToken
from docsie_universal_importer.providers import registry
from .provider import Provider
from .serializers import ConnectorTokenSerializer


def get_provider_cls(provider_id: str):
    return registry.by_id(provider_id)


class BaseView(APIView):
    provider: Provider

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
        serializer_cls = self.provider.get_import_serializer()
        serializer = serializer_cls(data=json.loads(request.body))
        serializer.is_valid(raise_exception=True)
        response = {'data': []}
        for file, content in self.provider.download_files():
            import_adapter = self.provider.get_import_adapter()
            retval = import_adapter.import_content(request, file, content, **serializer.data)
            response['data'].append(retval)

        return Response(data=response, status=200)


class ConnectorTokenListView(BaseView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = ConnectorToken.objects.filter(provider=self.provider.id, user=request.user)
        serializer = ConnectorTokenSerializer(queryset, many=True)

        return Response(data=serializer.data, status=200)
