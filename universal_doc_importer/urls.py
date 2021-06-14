from django.urls import path

from .views import GithubRepoMapView

urlpatterns = [
    path('github/repo/', GithubRepoMapView.as_view(), name='github_repo_map'),
]
