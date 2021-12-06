from docsie_universal_importer.providers.base.urls import default_urlpatterns

from .import_provider import URLOAuth2Provider

urlpatterns = default_urlpatterns(URLOAuth2Provider)
