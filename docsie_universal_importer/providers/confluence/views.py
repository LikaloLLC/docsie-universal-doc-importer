from docsie_universal_importer import app_settings
from docsie_universal_importer.providers.base import StorageTreeView, ImporterView, ConnectorTokenListView
from docsie_universal_importer.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView
from .import_provider import ConfluenceOAuth2Provider


class ConfluenceOAuth2Adapter(OAuth2Adapter):
    provider_id = ConfluenceOAuth2Provider.id
    access_token_url = "https://auth.atlassian.com/oauth/token"
    authorize_url = "https://auth.atlassian.com/authorize"
    audience = 'api.atlassian.com'


login_view = OAuth2LoginView.adapter_view(ConfluenceOAuth2Adapter)
callback_view = app_settings.OAUTH2_CALLBACK_VIEW.adapter_view(ConfluenceOAuth2Adapter)
storage_view = StorageTreeView.provider_view(ConfluenceOAuth2Provider)
importer_view = ImporterView.provider_view(ConfluenceOAuth2Provider)
token_list_view = ConnectorTokenListView.provider_view(ConfluenceOAuth2Adapter)
