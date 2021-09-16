from docsie_universal_importer.providers.base.urls import default_urlpatterns

from .import_provider import GitlabOAuth2Provider

urlpatterns = default_urlpatterns(GitlabOAuth2Provider)
