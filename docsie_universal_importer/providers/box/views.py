from docsie_universal_importer import app_settings
from docsie_universal_importer.providers.base import StorageTreeView, ImporterView, ConnectorTokenListView
from docsie_universal_importer.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView
from .import_provider import BoxOAuth2Provider


class BoxOAuth2Adapter(OAuth2Adapter):
    provider_id = BoxOAuth2Provider.id
    access_token_url = "https://api.box.com/oauth2/token"
    authorize_url = "https://account.box.com/api/oauth2/authorize"


login_view = OAuth2LoginView.adapter_view(BoxOAuth2Adapter)
callback_view = app_settings.OAUTH2_CALLBACK_VIEW.adapter_view(BoxOAuth2Adapter)
storage_view = StorageTreeView.provider_view(BoxOAuth2Provider)
importer_view = ImporterView.provider_view(BoxOAuth2Provider)
token_list_view = ConnectorTokenListView.provider_view(BoxOAuth2Adapter)
