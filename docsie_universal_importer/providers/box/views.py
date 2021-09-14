from docsie_universal_importer.providers.base import StorageTreeView, ImporterView
from docsie_universal_importer.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView, OAuth2CallbackView
from .import_provider import BoxOAuth2Provider


class BoxOAuth2Adapter(OAuth2Adapter):
    provider_id = BoxOAuth2Provider.id
    access_token_url = "https://api.box.com/oauth2/token"
    authorize_url = "https://account.box.com/api/oauth2/authorize"


login_view = OAuth2LoginView.adapter_view(BoxOAuth2Adapter)
callback_view = OAuth2CallbackView.adapter_view(BoxOAuth2Adapter)
storage_view = StorageTreeView.provider_view(BoxOAuth2Provider)
importer_view = ImporterView.provider_view(BoxOAuth2Provider)
