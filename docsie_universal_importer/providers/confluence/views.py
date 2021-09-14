from docsie_universal_importer.providers.base import StorageTreeView, ImporterView
from docsie_universal_importer.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView, OAuth2CallbackView
from .import_provider import ConfluenceOAuth2Provider


class ConfluenceOAuth2Adapter(OAuth2Adapter):
    provider_id = ConfluenceOAuth2Provider.id
    access_token_url = "https://auth.atlassian.com/oauth/token"
    authorize_url = "https://auth.atlassian.com/authorize"
    audience = 'api.atlassian.com'


login_view = OAuth2LoginView.adapter_view(ConfluenceOAuth2Adapter)
callback_view = OAuth2CallbackView.adapter_view(ConfluenceOAuth2Adapter)
storage_view = StorageTreeView.provider_view(ConfluenceOAuth2Provider)
importer_view = ImporterView.provider_view(ConfluenceOAuth2Provider)
