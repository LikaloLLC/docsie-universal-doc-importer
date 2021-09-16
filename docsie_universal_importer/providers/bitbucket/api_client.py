from urllib.parse import urlparse

import requests
from atlassian.bitbucket.cloud import Cloud


class BitbucketAPIClient:
    api_url: str = 'https://api.bitbucket.org/2.0/'

    def __init__(self, token):
        self._token = token

    def get_header(self):
        """
        Return the request header
        :return:
        """
        headers = {'Authorization': f'Bearer {self._token}'}
        return headers

    def get_content(self, repo_name, path_file, ref):
        """
        Returns the content of the given file
        :param repo_name:
        :param path_file:
        :return:
        """
        url = self.get_contents_endpoint_url(repo_name, path_file, ref)
        return requests.get(url=url, headers=self.get_header()).json()['values']

    def get_file_content(self, repo_name, filepath, ref):
        url = self.get_contents_endpoint_url(repo_name, filepath, ref)

        return requests.get(url=url, headers=self.get_header()).content

    def get_contents_endpoint_url(self, repo_name, filepath, ref) -> str:
        return self.api_url + 'repositories/' + repo_name + f'/src/{ref}/' + filepath + '?ref=' + ref


class BitbucketAPIConnector:
    def __init__(self, client_id, token):
        self._client_id = client_id
        self._token = token

        self.client = BitbucketAPIClient(self._token)
        token = {
            'access_token': token,
            'token_type': 'bearer'
        }
        oauth2_dict = {
            "client_id": client_id,
            "token": token
        }
        self.cloud = Cloud(
            url='https://api.bitbucket.org/',
            oauth2=oauth2_dict
        )

    def get_content(self, repo, path, ref):
        """
        Return content of the given path file
        :param repo:
        :param path:
        :param ref:
        :return:
        """
        return self.client.get_content(repo, path, ref)

    def get_file_content(self, repo, path, ref):
        return self.client.get_file_content(repo, path, ref)

    def get_user_repo(self, repo_name):
        """
        Return user`s repository
        :param repo_name:
        :return:
        """
        return repo_name

    def get_default_branch(self, repo) -> str:
        repo, branch = repo.split('/', 1)[0], ''
        repository = self.cloud.repositories.get(repo)
        return repository['values'][0]['mainbranch']['name']

    def _parse_url(self, url: str) -> tuple:
        """
        Parse the given url and return repository name, branch and path to the file or directory
        :param url:
        :return: tuple
        """
        # Return repo name, branch name, path to file
        uri = urlparse(url)
        urls = uri.path
        repo_name, path = urls.split('src')

        repo_name, branch = repo_name.strip('/'), path.split('/')[1]
        path = path.replace('/' + branch + '/', '')
        repo_name = repo_name.strip('-').strip('/')
        owner, repo_name = repo_name.split('/')
        return owner, repo_name, branch, path
