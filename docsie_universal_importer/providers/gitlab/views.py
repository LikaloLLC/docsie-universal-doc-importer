from docsie_universal_importer.providers.base import StorageTreeView, ImporterView
from docsie_universal_importer.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView, OAuth2CallbackView
from .import_provider import GitlabOAuth2Provider


class GitlabOAuth2Adapter(OAuth2Adapter):
    provider_id = GitlabOAuth2Provider.id

    provider_default_url = "https://gitlab.com"
    provider_api_version = "v4"

    access_token_url = "{0}/oauth/token".format(provider_default_url)
    authorize_url = "{0}/oauth/authorize".format(provider_default_url)


login_view = OAuth2LoginView.adapter_view(GitlabOAuth2Adapter)
callback_view = OAuth2CallbackView.adapter_view(GitlabOAuth2Adapter)
storage_view = StorageTreeView.provider_view(GitlabOAuth2Provider)
importer_view = ImporterView.provider_view(GitlabOAuth2Provider)
