from docsie_universal_importer.providers.base import StorageTreeView, ImporterView
from docsie_universal_importer.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView, OAuth2CallbackView
from .import_provider import GithubOAuth2Provider


class GithubOAuth2Adapter(OAuth2Adapter):
    provider_id = GithubOAuth2Provider.id

    access_token_url = "https://github.com/login/oauth/access_token"
    authorize_url = "https://github.com/login/oauth/authorize"


login_view = OAuth2LoginView.adapter_view(GithubOAuth2Adapter)
callback_view = OAuth2CallbackView.adapter_view(GithubOAuth2Adapter)
storage_view = StorageTreeView.provider_view(GithubOAuth2Provider)
importer_view = ImporterView.provider_view(GithubOAuth2Provider)
