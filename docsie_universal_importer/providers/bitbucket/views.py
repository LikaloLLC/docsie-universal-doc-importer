from docsie_universal_importer import app_settings
from docsie_universal_importer.providers.base import StorageTreeView, ImporterView, ConnectorTokenListView
from docsie_universal_importer.providers.oauth2.views import OAuth2Adapter, OAuth2LoginView
from .import_provider import BitbucketOAuth2Provider


class BitbucketOAuth2Adapter(OAuth2Adapter):
    provider_id = BitbucketOAuth2Provider.id

    access_token_url = "https://bitbucket.org/site/oauth2/access_token"
    authorize_url = "https://bitbucket.org/site/oauth2/authorize"


login_view = OAuth2LoginView.adapter_view(BitbucketOAuth2Adapter)
callback_view = app_settings.OAUTH2_CALLBACK_VIEW.adapter_view(BitbucketOAuth2Adapter)
storage_view = StorageTreeView.provider_view(BitbucketOAuth2Provider)
importer_view = ImporterView.provider_view(BitbucketOAuth2Provider)
token_list_view = ConnectorTokenListView.provider_view(BitbucketOAuth2Provider)
