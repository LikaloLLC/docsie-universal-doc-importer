from docsie_universal_importer.providers.base.urls import default_urlpatterns

from .import_provider import BoxOAuth2Provider

urlpatterns = default_urlpatterns(BoxOAuth2Provider)
