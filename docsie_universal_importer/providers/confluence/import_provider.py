import os

import requests
from bs4 import BeautifulSoup

from docsie_universal_importer.providers.base import (
    StorageViewer, StorageTree,
    Downloader, DownloaderAdapter,
    StorageViewerAdapter
)
from .file import ConfluenceFile
from .serializers import ConfluenceStorageTreeRequestSerializer, ConfluenceDownloaderSerializer
from ..oauth2.provider import OAuth2Provider


class ConfluenceConnector:
    def __init__(self, token):
        """
        :param: token: 2OAuth token for Confluence
        :param: instance_id: Instance id where needs to import content
        """
        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }
        self.cloud_id = self._get_cloud_id()
        self.cloud_name = self._get_site_name()
        self.base_url = f'https://api.atlassian.com/ex/confluence/{self.cloud_id}/rest/api/content'
        self.current_attachments = {}

    def _get_cloud_id(self):
        r = requests.get('https://api.atlassian.com/oauth/token/accessible-resources', headers=self.headers)
        return r.json()[0]['id']

    def _get_site_name(self):
        r = requests.get('https://api.atlassian.com/oauth/token/accessible-resources', headers=self.headers)
        return r.json()[0]['name']

    def _request(self, endpoint: str):
        if not endpoint[:1] == '/':  # adding slash pre endpoint if you forgot adding this
            endpoint = '/' + endpoint

        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers)

        return response

    def get_page_content(self, page_id):
        endpoint = f'{page_id}?expand=body.storage'
        response = self._request(endpoint)
        return response.json()['body']['storage']['value']

    def get_page(self, page_id):
        endpoint = f'{page_id}?expand=body.storage'
        response = self._request(endpoint)
        parsed = BeautifulSoup(response.json()['body']['storage']['value'], 'html.parser')
        self.current_attachments = self.get_attachments(page_id)

        # adding page title
        pagetitle = parsed.new_tag('pagetitle')
        pagetitle.string = response.json().get('title', 'Confluence')
        parsed.append(pagetitle)
        for img in parsed.find_all('ri:attachment'):
            img['url'] = self.get_image_url(img)
        return str(parsed)

    def list_pages_ids(self, page_id='/'):
        response = self._request(page_id).json()  # request to the base url
        return response.get('results')

    def get_image_url(self, image_tag: BeautifulSoup.findAll):
        file_name = image_tag['ri:filename']
        image_json = self.current_attachments.get(str(file_name))

        download_url = f'https://{self.cloud_name}.atlassian.net/wiki/{image_json["_links"]["download"]}'
        output_url = download_url

        return output_url

    def get_attachments(self, page_id):
        endpoint = f'{page_id}/child/attachment'

        response = self._request(endpoint)
        attachments = {}
        for attach in response.json().get('results', []):
            attachments.update(
                {attach['title']: attach}
            )
        return attachments


class ConfluenceStorageViewer(StorageViewer):
    file_cls = ConfluenceFile

    def __init__(self, client: ConfluenceConnector):
        self.client = client

    def init_storage_tree(self) -> StorageTree:
        return StorageTree('.')

    def get_external_files(self):
        pages_ids = self.client.list_pages_ids()
        while pages_ids:
            file_obj = pages_ids.pop(0)

            yield os.path.dirname(file_obj.get('title')), file_obj


class ConfluenceDownloader(Downloader):
    file_cls = ConfluenceFile

    def __init__(self, client: ConfluenceConnector):
        self.client = client

    def download_file(self, file: ConfluenceFile):
        return self.client.get_page(file.id)


class ConfluenceDownloaderAdapter(DownloaderAdapter):
    adapted_cls = ConfluenceDownloader
    request_serializer_cls = ConfluenceDownloaderSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']

        client = ConfluenceConnector(token=token)

        return {'client': client}


class ConfluenceStorageViewerAdapter(StorageViewerAdapter):
    adapted_cls = ConfluenceStorageViewer
    request_serializer_cls = ConfluenceStorageTreeRequestSerializer

    def get_adapted_init_kwargs(self, validated_data: dict):
        token = validated_data['token']

        client = ConfluenceConnector(token=token)

        return {'client': client}


class ConfluenceOAuth2Provider(OAuth2Provider):
    id = 'confluence'
    audience = 'api.atlassian.com'
    storage_viewer_adapter_cls = ConfluenceStorageViewerAdapter
    downloader_adapter_cls = ConfluenceDownloaderAdapter


provider_classes = [ConfluenceOAuth2Provider]
