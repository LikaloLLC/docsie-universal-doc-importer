from django.db.models import ObjectDoesNotExist
from django.http import Http404
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from rest_framework.views import APIView
from swag_auth.models import SwaggerStorage

from universal_doc_importer.registry import connector_registry


class RepoMapView(APIView):
    def get_storage(self, url) -> 'SwaggerStorage':
        try:
            swagger = SwaggerStorage.objects.filter(user=self.request.user, url=url).last()
            if swagger is None:
                raise Http404
            return swagger

        except (ObjectDoesNotExist, MultiValueDictKeyError):
            raise Http404

    def get_importer(self, connector_id):
        connector_registry.get_list()
        return connector_registry.by_id(connector_id)

    def get(self, request) -> 'Response':
        # Get repo map and return it to the user
        url = self.request.query_params['url']
        swagger_storage = self.get_storage(url)
        connector_id = swagger_storage.token.connector
        importer_cls = self.get_importer(connector_id)

        importer = importer_cls(swagger_storage.token.token)
        status = 200
        try:
            extensions = self.get_extensions_from_query_params()
            data = importer.get_repo_map(swagger_storage.url, extensions=extensions)
        except Exception as e:
            data = {'error': str(e)}
            status = 400

        return Response(data=data, status=status)

    def get_extensions_from_query_params(self):
        extensions_str = self.request.query_params.get('extensions')
        if extensions_str:
            extensions = extensions_str.replace(' ', '').split(',')
        else:
            extensions = ['md']
        return extensions
