from django.db.models import ObjectDoesNotExist
from django.http import Http404
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from rest_framework.views import APIView
from swag_auth.models import SwaggerStorage

from universal_doc_importer.registry import connector_registry


class GithubRepoMapView(APIView):
    def get_storage(self, request) -> 'SwaggerStorage':
        try:

            url = self.request.query_params['url']
            swagger = SwaggerStorage.objects.filter(user=request.user, url=url).last()
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
        swagger_storage = self.get_storage(request)
        connector_id = swagger_storage.token.connector
        importer_cls = self.get_importer(connector_id)

        importer = importer_cls(swagger_storage.token.token)
        status = 200
        try:
            extensions_str = self.request.query_params.get('extensions')
            if extensions_str:
                extensions = extensions_str.replace(' ', '').split(',')
            else:
                extensions = ['md']
            data = importer.get_repo_map(swagger_storage.url, extensions=extensions)
        except Exception as e:
            data = {'error': e}
            status = 400

        return Response(data=data, status=status)
