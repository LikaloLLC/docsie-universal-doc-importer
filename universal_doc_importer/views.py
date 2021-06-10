from django.db.models import ObjectDoesNotExist
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from swag_auth.models import SwaggerStorage

from universal_doc_importer.registry import registry


class GithubRepoMapView(APIView):
    def get_storage(self, request) -> 'SwaggerStorage':
        try:
            return SwaggerStorage.objects.filter(user=request.user).last()
        except ObjectDoesNotExist:
            raise Http404

    def get_importer(self, connector_id):
        return registry.by_id(connector_id)

    def get(self, request) -> 'Response':
        # Get repo map and return it to the user
        swagger_storage = self.get_storage(request)
        connector_id = swagger_storage.token.connector
        provider = self.get_importer(connector_id)
        importer = provider(swagger_storage.token)
        status = 200
        try:
            data = importer.get_repo_map(swagger_storage.url, extensions=request.GET.get('extensions', ['md']))
        except Exception as e:
            data = {'error': e}
            status = 400

        return Response(data=data, status=status)
