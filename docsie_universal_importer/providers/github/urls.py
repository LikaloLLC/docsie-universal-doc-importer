from docsie_universal_importer.providers.base.urls import default_urlpatterns

from .import_provider import GithubOAuth2Provider

urlpatterns = default_urlpatterns(GithubOAuth2Provider)
