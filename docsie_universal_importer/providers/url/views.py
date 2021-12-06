from docsie_universal_importer.providers.base import ImporterView
from .import_provider import URLOAuth2Provider

importer_view = ImporterView.provider_view(URLOAuth2Provider)
