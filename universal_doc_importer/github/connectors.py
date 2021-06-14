from urllib.parse import urlparse

from swag_auth.github.connectors import GithubAPIConnector

from universal_doc_importer.file_system import FileSystem
from universal_doc_importer.utils import filter_by_extension


class GithubImporter(GithubAPIConnector):
    provider_id = 'github'

    def _parse_url(self, url: str) -> str:
        uri = urlparse(url)
        urls = uri.path
        if urls.count('blob'):
            div_str = 'blob'
        elif urls.count('tree'):
            div_str = 'tree'
        else:
            urls = urls + '/blob/'
            div_str = 'blob'
        repo_name, path = urls.split(div_str)

        repo_name, branch = repo_name.strip('/'), path.split('/')[1]
        repo_name = repo_name.strip('-')
        repo_name = repo_name.strip('/')

        return repo_name

    def get_repo_map(self, url, extensions):
        repo_name = self._parse_url(url=url)
        folder_name = repo_name.split('/')[1]
        repo = self.get_user_repo(repo_name)

        contents = repo.get_contents("")
        records = []
        myFile = FileSystem(folder_name)
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))

            records.append(file_content.path)
            extension = file_content.path.split('.')[-1]
            if extension in extensions or file_content.path == extension:
                myFile.addChild(file_content.path)
        result = filter_by_extension(myFile.makeDict(), extensions)
        return result


connector_classes = [GithubImporter]
