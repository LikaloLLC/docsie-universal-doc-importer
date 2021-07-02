from swag_auth.github.connectors import GithubSwaggerDownloader

from docsie_universal_importer.mixin import ImporterMixin


class GithubImporter(GithubSwaggerDownloader, ImporterMixin):
    provider_id = 'github'

    def get_contents(self, repo, path, branch):
        return repo.get_contents(path="", ref=branch)

    def get_repo_paths(self, contents, repo, branch):
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(self.get_contents(repo, file_content.path, branch))
            else:
                yield f'{branch}/{file_content.path}'


connector_classes = [GithubImporter]
