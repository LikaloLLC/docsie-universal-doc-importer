from swag_auth.gitlab.connectors import GitlabSwaggerDownloader

from docsie_universal_importer.mixin import ImporterMixin


class GitlabImporter(GitlabSwaggerDownloader, ImporterMixin):
    provider_id = 'gitlab'

    def get_contents(self, repo, path, branch):
        return repo.repository_tree(path, branch)

    def get_repo_paths(self, contents, repo, branch):
        while contents:
            file_content = contents.pop(0)
            if file_content['type'] == "tree":
                contents.extend(self.get_contents(repo, file_content.path, branch))
            else:
                yield f'{branch}/{file_content["path"]}'


connector_classes = [GitlabImporter]
