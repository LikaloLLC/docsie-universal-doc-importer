# docsie-universal-doc-importer
Python/Django library to import documentation from anywhere and send it to anywhere. Made by [Docsie](https://www.docsie.io).

The primary goal of this library is to serve as a universal interface for importing docs to your app. The idea here is to provide django developers with a familiar 
interface to build import/export modules for their app, so they no longer need to write their own code. 

We appretiate any help and support for this module and look forward to seeing your comments. 


## Current List of Adapters
- Github
- Gitlab
- Bitbucket
- Google Drive
- Dropbox
- Box
- Google Cloud Storage

## Adapters on the roadmap
- Confluence
- Swaggerhub
- HTML
- S3
- Azure Blob Storage


# Getting started

## Install

```bash
$ pip3 install git+https://github.com/LikaloLLC/docsie-universal-doc-importer
```

## Migrate
```bash
python manage.py migrate
```


## Configurations
### 1. project_name/settings.py
```
INSTALLED_APPS = [
    ...
    'django.contrib.sites',

    # rest-framework apps
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'rest_auth.registration',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',

    # universal importer
    'docsie_universal_importer',
    
    # Providers
    'docsie_universal_importer.providers.github',
    'docsie_universal_importer.providers.gitlab',
    'docsie_universal_importer.providers.bitbucket',
    'docsie_universal_importer.providers.confluence',
    'docsie_universal_importer.providers.box',
    'docsie_universal_importer.providers.google_drive',
    'docsie_universal_importer.providers.google_cloud_storage',
    ...
]

UNIVERSAL_DOC_IMPORTER_IMPORT_ADAPTER = 'path.to.Adapter'  # Adapter that receives downloaded content.
UNIVERSAL_DOC_IMPORTER_SERIALIZER = path.to.ImportParamsSerializer'  # Serializer with additional fields,
                                                                     # that are passed into import endpoint.
UNIVERSAL_DOC_IMPORTER_PROVIDERS = {
    'github': {
        'import_adapter': 'app.adapters.GithubImportAdapter',  # Overrides UNIVERSAL_DOC_IMPORTER_IMPORT_ADAPTER setting.
        
        # OAuth application credentials
        'APP': {
            'client_id': env.str('GITHUB_CLIENT_ID'),
            'secret': env.str('GITHUB_SECRET'),
            'key': '',
        },
        
        # OAuth scope
        'SCOPE': [
            'repo',
        ],
    },
    ...
}

```

### 2. project_name/urls.py
```
    path('importer/', include('docsie_universal_importer.urls')),
    path('account/', include('rest_auth.urls'))
```
