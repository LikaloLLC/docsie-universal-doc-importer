from docsie_universal_importer.providers.base import StorageTreeView, ImporterView
from docsie_universal_importer.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView, OAuth2CallbackView
from .import_provider import GoogleCloudStorageOAuth2Provider


class GoogleCloudStorageOAuth2Adapter(OAuth2Adapter):
    provider_id = GoogleCloudStorageOAuth2Provider.id

    access_token_url = "https://accounts.google.com/o/oauth2/token"
    authorize_url = "https://accounts.google.com/o/oauth2/auth"


login_view = OAuth2LoginView.adapter_view(GoogleCloudStorageOAuth2Adapter)
callback_view = OAuth2CallbackView.adapter_view(GoogleCloudStorageOAuth2Adapter)
storage_view = StorageTreeView.provider_view(GoogleCloudStorageOAuth2Provider)
importer_view = ImporterView.provider_view(GoogleCloudStorageOAuth2Provider)
