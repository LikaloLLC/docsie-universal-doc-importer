from allauth.utils import import_attribute
from django.urls import path, include


def default_urlpatterns(connector):
    login_view = import_attribute(connector.get_package() + ".views.login_view")
    callback_view = import_attribute(connector.get_package() + ".views.callback_view")
    storage_view = import_attribute(connector.get_package() + ".views.storage_view")
    import_view = import_attribute(connector.get_package() + ".views.importer_view")

    urlpatterns = [
        path('login/', login_view, name=connector.id + '_universal_importer_login'),
        path('callback/', callback_view, name=connector.id + '_universal_importer_callback'),
        path("storage/", storage_view, name=connector.id + "_storage"),
        path("import/", import_view, name=connector.id + "_import"),
    ]
    return [path(connector.get_slug() + "/", include(urlpatterns))]
