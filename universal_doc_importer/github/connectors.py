from urllib.parse import urlparse

from swag_auth.github.connectors import GithubAPIConnector

from universal_doc_importer.file_system import FileSystem


class GithubImporter(GithubAPIConnector):
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

    def get_repo_map(self, url, extensions='md'):
        repo_name = self._parse_url(url=url)
        folder_name = repo_name.split('/')[1]
        repo = self.get_user_repo(repo_name)

        contents = repo.get_contents("")
        records = []
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            records.append(file_content.path)

        myFile = FileSystem(folder_name)
        for record in records[1:]:
            myFile.addChild(record)
        return myFile.makeDict()
