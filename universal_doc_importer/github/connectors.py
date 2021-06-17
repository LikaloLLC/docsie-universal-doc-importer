import os
from urllib.parse import urlparse

from swag_auth.github.connectors import GithubAPIConnector

from universal_doc_importer.repo_map import RepositoryMap
from universal_doc_importer.utils import get_repo_content_path


class GithubImporter(GithubAPIConnector):
    provider_id = 'github'

    def _parse_url(self, url: str) -> str:
        uri = urlparse(url)
        urls = uri.path
        if 'blob' in urls:
            div_str = 'blob'
        elif 'tree' in urls:
            div_str = 'tree'
        else:
            urls = urls + '/blob/'
            div_str = 'blob'
        repo_name, path = urls.split(div_str)

        repo_name, branch = repo_name.strip('/'), path.split('/')[1]
        repo_name = repo_name.strip('-').strip('/')

        return repo_name

    def get_repo_map(self, url, extensions):
        repo_name = self._parse_url(url=url)
        folder_name = '-'.join(repo_name.split('/')[:2])
        repo = self.get_user_repo(repo_name)

        contents = repo.get_contents("")
        repo_map = RepositoryMap(folder_name, extensions)
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                extension = os.path.splitext(file_content.path)[1][1:]

                if extension in extensions:
                    repo_map.add_path(file_content.path)

        return repo_map.as_dict()

    def get_files(self, repo_map):
        repo_name = list(repo_map)[0]
        repo_name = '/'.join(repo_name.split('-', 1)[:2])
        urls = get_repo_content_path(repo_map)
        repo = self.get_user_repo(repo_name)
        for url in urls:
            content = self.get_swagger_content(repo, url)
            yield url, content


connector_classes = [GithubImporter]
