from docsie_universal_importer.providers.base.urls import default_urlpatterns

from .import_provider import GoogleDriveOAuth2Provider

urlpatterns = default_urlpatterns(GoogleDriveOAuth2Provider)
