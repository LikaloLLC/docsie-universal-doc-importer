from django.urls import path

from .views import RepoMapView

urlpatterns = [
    path('github/repo/', RepoMapView.as_view(), name='github_repo_map'),
]
