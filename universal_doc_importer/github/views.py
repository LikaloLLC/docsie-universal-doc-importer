from django.db.models import ObjectDoesNotExist
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from swag_auth.models import SwaggerStorage

from universal_doc_importer.github.connectors import GithubImporter


class GithubRepoMapView(APIView):
    def get_storage(self, request) -> 'SwaggerStorage':
        try:
            url = self.request.query_params['url']
            return SwaggerStorage.objects.filter(user=request.user, url=url).last()
        except (ObjectDoesNotExist, KeyError):
            raise Http404

    def get(self, request) -> 'Response':
        # Get repo map and return it to the user
        swagger_storage = self.get_storage(request)
        importer = GithubImporter(swagger_storage.token)
        status = 200
        try:
            data = importer.get_repo_map(swagger_storage.url, extensions=request.GET.get('extensions', ['md']))
        except Exception as e:
            data = {'error': e}
            status = 400

        return Response(data=data, status=status)
