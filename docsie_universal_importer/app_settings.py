import sys

from docsie_universal_importer.utils import import_attribute


class AppSettings:
    def __init__(self, prefix):
        self.prefix = prefix

    def _setting(self, name, default):
        from django.conf import settings

        return getattr(settings, self.prefix + name, default)

    @property
    def PROVIDERS(self):
        """Provider specific settings"""
        return self._setting("PROVIDERS", {})

    @property
    def IMPORT_ADAPTER(self):
        return self._setting("ADAPTER", '')

    @property
    def IMPORT_SERIALIZER(self):
        return self._setting('SERIALIZER', '')

    @property
    def ALLOWED_EXTENSIONS(self):
        return self._setting('ALLOWED_EXTENSIONS', '*')

    @property
    def OAUTH2_CALLBACK_VIEW(self):
        path_to_callback = self._setting('OAUTH2_CALLBACK_VIEW',
                                         'docsie_universal_importer.providers.oauth2.views.OAuth2CallbackView')

        return import_attribute(path_to_callback)


app_settings = AppSettings("UNIVERSAL_DOC_IMPORTER_")
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
