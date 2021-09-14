from docsie_universal_importer.providers.base.urls import default_urlpatterns

from .import_provider import BitbucketOAuth2Provider

urlpatterns = default_urlpatterns(BitbucketOAuth2Provider)
