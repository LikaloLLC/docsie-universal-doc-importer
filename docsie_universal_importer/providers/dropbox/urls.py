from docsie_universal_importer.providers.base.urls import default_urlpatterns

from .import_provider import DropboxOAuth2Provider

urlpatterns = default_urlpatterns(DropboxOAuth2Provider)
