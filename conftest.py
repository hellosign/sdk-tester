import pytest
import sys
import os

import json
import base64

scriptdir = os.path.dirname(os.path.realpath(__file__))
utilsdir = f'{scriptdir}/tests/utils/'
print(f"utils dir {utilsdir}")
sys.path.insert(0, utilsdir)
import helpers_hsapi

import requests
from string import Template, ascii_lowercase, digits


@pytest.fixture(scope='module')
def container_bin():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"dir path {dir_path}")

    container_bin = f'{dir_path}/run'
    return container_bin
    #

    # Grab the following from config file, environment, or somewhere else
    #
@pytest.fixture(scope='module')
def sdk_language():
    # One of "node", "php", "python", "ruby", "csharp", "java"
    sdk_language = os.environ['LANGUAGE']
    print(f"SDK Language : {sdk_language}")
    return sdk_language

@pytest.fixture(scope='module')
def uploads_dir():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"dir path {dir_path}")
    # Uploads directory, containing PDFs you may want to upload to the API
    uploads_dir = f'{dir_path}/file_uploads'
    print(f"File Upload directory : {uploads_dir}")
    return uploads_dir

@pytest.fixture
def auth_type():
    # One of "apikey" or "oauth"
    api_auth = 'apikey'
    return api_auth

@pytest.fixture
def auth_key():
    # The API key or OAuth bearer token to use for the request
    auth_key = os.environ['API_KEY']
    return auth_key
@pytest.fixture
def server():
    # Change server, ie dev/qa/staging/prod
    server = os.environ['SERVER']
    return server

@pytest.fixture(scope='module')
def get_clientid():
    #HS_API_APP = 'Automation APP'
    res = helpers_hsapi.get_list_api_apps(page_size=30)
    res_json = json.loads(res.text)
    print(f"\nget list apps {res_json}")
    assert res.status_code == 200
    if len(res_json['api_apps']) > 0:
        client_id = res_json['api_apps'][0]['client_id']
        print(f"\nClient ID :: {client_id}")
        return client_id
    # for app_num in range(len(res_json['api_apps'])):
    #     if res_json['api_apps'][app_num]['name'] == HS_API_APP:
    #         # Get the client_id
    #         print(f"App Name found ::  {res_json['api_apps'][app_num]['name']}")
    #         client_id = res_json['api_apps'][app_num]['client_id']
    #         print(f"Client ID :: {client_id}")
    #         return client_id






