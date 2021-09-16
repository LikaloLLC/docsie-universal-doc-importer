from docsie_universal_importer.providers.base.urls import default_urlpatterns

from .import_provider import ConfluenceOAuth2Provider

urlpatterns = default_urlpatterns(ConfluenceOAuth2Provider)
