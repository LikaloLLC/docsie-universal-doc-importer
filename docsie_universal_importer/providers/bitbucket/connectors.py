from swag_auth.bitbucket.connectors import BitbucketSwaggerDownloader

from docsie_universal_importer.mixin import ImporterMixin


class BitbucketImporter(BitbucketSwaggerDownloader, ImporterMixin):
    provider_id = 'bitbucket'

    def get_contents(self, repo, path, branch):
        return self.get_file_content(repo=repo, path=path, ref=branch)

    def get_repo_paths(self, contents, repo, branch):

        while contents:
            file_content = contents.pop(0)
            if file_content.get('type') == "commit_directory":
                contents.extend(self.get_contents(repo, file_content.get('path'), branch))
            else:
                yield f'{branch}/{file_content.get("path")}'


connector_classes = [BitbucketImporter]
