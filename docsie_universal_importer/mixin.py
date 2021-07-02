import os

from docsie_universal_importer.repo_map import RepositoryMap
from docsie_universal_importer.utils import get_repo_content_path


class ImporterMixin:
    def get_repo_map(self, url, extensions):
        owner, repo_name, branch, path = self.parse_url(url)

        repo = self.get_user_repo(f'{owner}/{repo_name}')
        contents = self.get_contents(repo, path, branch)

        repo_map = RepositoryMap(repo_name, extensions)
        for path in self.get_repo_paths(contents, repo, branch):
            # Check extension
            extension = os.path.splitext(path)[1][1:]
            if extension in extensions:
                repo_map.add_path(path)

        return {owner: repo_map.as_dict()}

    def get_files(self, repo_map):
        owner, repo_name, branch = None, None, None
        for key, value in repo_map.items():
            owner, repo_name, repo_map = key, list(value)[0], value
            break
        urls = get_repo_content_path(repo_map)
        repo = self.get_user_repo(f'{owner}/{repo_name}')
        for url in urls:
            branch, url = url.split('/', 1)[0], url.split('/', 1)[1]
            content = self.get_file_content(repo, url, branch)
            yield url, content

    def parse_url(self, url: str) -> tuple:
        owner, repo_name, branch, path = self._parse_url(url=url)
        repo = self.get_user_repo(f'{owner}/{repo_name}')
        if not branch:
            branch = self.get_default_branch(repo)
        return owner, repo_name, branch, path

    def get_contents(self, repo, path, branch):
        raise NotImplementedError

    def get_repo_paths(self, contents, repo, branch):
        raise NotImplementedError
