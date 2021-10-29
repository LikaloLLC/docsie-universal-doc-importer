from docsie_universal_importer import app_settings
from docsie_universal_importer.providers.base import StorageTreeView, ImporterView, ConnectorTokenListView
from docsie_universal_importer.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView
from .import_provider import GithubOAuth2Provider


class GithubOAuth2Adapter(OAuth2Adapter):
    provider_id = GithubOAuth2Provider.id

    access_token_url = "https://github.com/login/oauth/access_token"
    authorize_url = "https://github.com/login/oauth/authorize"


login_view = OAuth2LoginView.adapter_view(GithubOAuth2Adapter)
callback_view = app_settings.OAUTH2_CALLBACK_VIEW.adapter_view(GithubOAuth2Adapter)
storage_view = StorageTreeView.provider_view(GithubOAuth2Provider)
importer_view = ImporterView.provider_view(GithubOAuth2Provider)
token_list_view = ConnectorTokenListView.provider_view(GithubOAuth2Provider)
