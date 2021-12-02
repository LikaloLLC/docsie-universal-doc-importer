from docsie_universal_importer import app_settings
from docsie_universal_importer.providers.base import StorageTreeView, ImporterView, ConnectorTokenListView
from docsie_universal_importer.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView
from .import_provider import DropboxOAuth2Provider


class DropboxOAuth2Adapter(OAuth2Adapter):
    provider_id = DropboxOAuth2Provider.id

    access_token_url = "https://api.dropbox.com/oauth2/token"
    authorize_url = "https://www.dropbox.com/oauth2/authorize"


login_view = OAuth2LoginView.adapter_view(DropboxOAuth2Adapter)
callback_view = app_settings.OAUTH2_CALLBACK_VIEW.adapter_view(DropboxOAuth2Adapter)
storage_view = StorageTreeView.provider_view(DropboxOAuth2Provider)
importer_view = ImporterView.provider_view(DropboxOAuth2Provider)
token_list_view = ConnectorTokenListView.provider_view(DropboxOAuth2Provider)
