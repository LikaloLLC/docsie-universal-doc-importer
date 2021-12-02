from docsie_universal_importer import app_settings
from docsie_universal_importer.providers.base import StorageTreeView, ImporterView, ConnectorTokenListView
from docsie_universal_importer.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView
from .import_provider import GitlabOAuth2Provider


class GitlabOAuth2Adapter(OAuth2Adapter):
    provider_id = GitlabOAuth2Provider.id

    provider_default_url = "https://gitlab.com"
    provider_api_version = "v4"

    access_token_url = "{0}/oauth/token".format(provider_default_url)
    authorize_url = "{0}/oauth/authorize".format(provider_default_url)


login_view = OAuth2LoginView.adapter_view(GitlabOAuth2Adapter)
callback_view = app_settings.OAUTH2_CALLBACK_VIEW.adapter_view(GitlabOAuth2Adapter)
storage_view = StorageTreeView.provider_view(GitlabOAuth2Provider)
importer_view = ImporterView.provider_view(GitlabOAuth2Provider)
token_list_view = ConnectorTokenListView.provider_view(GitlabOAuth2Provider)
