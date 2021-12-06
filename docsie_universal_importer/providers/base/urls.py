from allauth.utils import import_attribute
from django.urls import path, include


def default_urlpatterns(connector):
    url_config = (
        ('.views.login_view', 'login/', '_universal_importer_login'),
        ('.views.callback_view', 'callback/', '_universal_importer_callback'),
        ('.views.storage_view', 'storage/', '_storage'),
        ('.views.importer_view', 'import/', '_import'),
        ('.views.token_list_view', 'tokens/', '_token_list'),
    )
    urlpatterns = []
    for view_path, url, url_suffix in url_config:
        try:
            view = import_attribute(connector.get_package() + view_path)
        except AttributeError:
            pass
        else:
            urlpatterns.append(
                path(url, view, name=connector.id + url_suffix)
            )

    return [path(connector.get_slug() + "/", include(urlpatterns))]
