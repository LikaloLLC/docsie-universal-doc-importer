from docsie_universal_importer import app_settings
from docsie_universal_importer.providers.base import StorageTreeView, ImporterView, ConnectorTokenListView
from docsie_universal_importer.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView
from .import_provider import GoogleDriveOAuth2Provider


class GoogleDriveOAuth2Adapter(OAuth2Adapter):
    provider_id = GoogleDriveOAuth2Provider.id

    access_token_url = "https://accounts.google.com/o/oauth2/token"
    authorize_url = "https://accounts.google.com/o/oauth2/auth"


login_view = OAuth2LoginView.adapter_view(GoogleDriveOAuth2Adapter)
callback_view = app_settings.OAUTH2_CALLBACK_VIEW.adapter_view(GoogleDriveOAuth2Adapter)
storage_view = StorageTreeView.provider_view(GoogleDriveOAuth2Provider)
importer_view = ImporterView.provider_view(GoogleDriveOAuth2Provider)
token_list_view = ConnectorTokenListView.provider_view(GoogleDriveOAuth2Adapter)
