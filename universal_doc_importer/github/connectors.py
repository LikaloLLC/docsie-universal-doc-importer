import os

from swag_auth.github.connectors import GithubSwaggerDownloader

from universal_doc_importer.repo_map import RepositoryMap
from universal_doc_importer.utils import get_repo_content_path


class GithubImporter(GithubSwaggerDownloader):
    provider_id = 'github'

    def get_repo_map(self, url, extensions):
        owner, repo_name, branch, path = self._parse_url(url=url)
        repo = self.get_user_repo(f'{owner}/{repo_name}')

        contents = repo.get_contents("")
        repo_map = RepositoryMap(repo_name, extensions)
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
            content = self.get_file_content(repo, url)
            yield url, content


connector_classes = [GithubImporter]
