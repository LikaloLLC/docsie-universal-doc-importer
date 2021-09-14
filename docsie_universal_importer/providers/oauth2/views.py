from datetime import timedelta

from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.helpers import render_authentication_error
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.base import AuthError, ProviderException
from allauth.socialaccount.providers.oauth2.client import OAuth2Error, OAuth2Client
from allauth.utils import get_request_param, build_absolute_uri
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from requests import RequestException

from docsie_universal_importer import providers
from docsie_universal_importer.models import ConnectorToken
from .provider import OAuth2Provider


class OAuth2Adapter:
    provider_id: str = None
    
    expires_in_key = "expires_in"
    client_class = OAuth2Client
    supports_state = True
    redirect_uri_protocol = None
    access_token_method = "POST"
    login_cancelled_error = "access_denied"
    scope_delimiter = " "
    basic_auth = False
    headers = None

    def __init__(self, request):
        self.request = request

    def get_provider(self) -> 'OAuth2Provider':
        return providers.registry.by_id(self.provider_id)(self.request)

    def get_callback_url(self, request):
        callback_url = reverse(self.provider_id + "_universal_importer_callback")
        protocol = self.redirect_uri_protocol
        return build_absolute_uri(request, callback_url, protocol)

    def parse_token(self, data):
        token = ConnectorToken(token=data['access_token'])
        token.token_secret = data.get('refresh_token', '')
        expires_in = data.get(self.expires_in_key, None)
        if expires_in:
            token.expires_at = timezone.now() + timedelta(seconds=int(expires_in))
        return token

    def get_access_token_data(self, request, client):
        code = get_request_param(self.request, "code")
        return client.get_access_token(code)

    def store_credentials(self, request, token: 'ConnectorToken'):
        """Save credentials in the ConnectorToken model."""
        token.provider = self.provider_id
        token.save()

        return token


class OAuth2View:
    adapter: 'OAuth2Adapter'

    @classmethod
    def adapter_view(cls, adapter):
        def view(request, *args, **kwargs):
            self = cls()
            self.request = request
            self.adapter = adapter(request)
            try:
                return self.dispatch(request, *args, **kwargs)
            except ImmediateHttpResponse as e:
                return e.response

        return view

    def get_client(self, request):
        callback_url = self.adapter.get_callback_url(request)
        provider = self.adapter.get_provider()
        settings = provider.get_settings()
        scope = provider.get_scope(request)
        client = self.adapter.client_class(
            self.request,
            settings['APP']['client_id'],
            settings['APP']['secret'],
            self.adapter.access_token_method,
            self.adapter.access_token_url,
            callback_url,
            scope,
            scope_delimiter=self.adapter.scope_delimiter,
            headers=self.adapter.headers,
            basic_auth=self.adapter.basic_auth,
        )
        return client


class OAuth2LoginView(OAuth2View):
    def dispatch(self, request, *args, **kwargs):
        client = self.get_client(request)
        auth_url = self.adapter.authorize_url
        client.state = SocialLogin.stash_state(request)
        try:
            return HttpResponseRedirect(client.get_redirect_url(auth_url, {}))
        except OAuth2Error as e:
            return render_authentication_error(request, self.adapter.provider_id, exception=e)


class OAuth2CallbackView(OAuth2View):
    def dispatch(self, request, *args, **kwargs):
        if "error" in request.GET or "code" not in request.GET:
            # Distinguish cancel from error
            auth_error = request.GET.get("error", None)
            if auth_error == self.adapter.login_cancelled_error:
                error = AuthError.CANCELLED
            else:
                error = AuthError.UNKNOWN
            return JsonResponse(status=400, data={
                "auth_error": {
                    "provider": self.adapter.provider_id,
                    "code": error,
                }
            })

        client = self.get_client(request)
        try:
            access_token = self.adapter.get_access_token_data(request, client)
            token = self.adapter.parse_token(access_token)
            self.adapter.store_credentials(request, token)

            return JsonResponse(status=200, data={'token': token.id})
        except (
                PermissionDenied,
                OAuth2Error,
                RequestException,
                ProviderException,
        ) as e:
            return JsonResponse(status=400, data={
                "auth_error": {
                    "provider": self.adapter.provider_id,
                    "error": e
                }
            })
