from urllib.parse import parse_qsl

from docsie_universal_importer.providers.base import Provider
from django.urls import reverse
from django.utils.http import urlencode


class OAuth2Provider(Provider):
    def get_login_url(self, request, **kwargs):
        url = reverse(self.id + '_universal_importer_login')
        if kwargs:
            url = url + '?' + urlencode(kwargs)
        return url

    def get_auth_params(self, request):
        settings = self.get_settings()
        ret = dict(settings.get('AUTH_PARAMS', {}))
        dynamic_auth_params = request.GET.get('auth_params', None)
        if dynamic_auth_params:
            ret.update(dict(parse_qsl(dynamic_auth_params)))
        return ret

    def get_scope(self, request):
        settings = self.get_settings()
        scope = list(settings.get('SCOPE', self.get_default_scope()))
        dynamic_scope = request.GET.get('scope', None)
        if dynamic_scope:
            scope.extend(dynamic_scope.split(','))
        return scope

    def get_default_scope(self):
        return []

