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
SUPPORTED_LANGUAGES = ("node", "php", "python", "ruby", "dotnet", "java")


def _selected_languages():
    """Resolve the set of SDK languages to exercise.

    Priority:
      1. LANGUAGES env var (comma-separated list, e.g. "python,node").
      2. LANGUAGE env var (single SDK) — kept for backwards compatibility.
      3. No default — fail loudly so a stray run cannot silently hit every SDK.
    """
    raw = os.environ.get("LANGUAGES") or os.environ.get("LANGUAGE")
    if not raw:
        raise RuntimeError(
            "Set LANGUAGES (comma-separated) or LANGUAGE (single value). "
            f"Supported: {', '.join(SUPPORTED_LANGUAGES)}."
        )

    langs = [item.strip().lower() for item in raw.split(",") if item.strip()]
    unknown = [item for item in langs if item not in SUPPORTED_LANGUAGES]
    if unknown:
        raise RuntimeError(
            f"Unsupported language(s): {', '.join(unknown)}. "
            f"Supported: {', '.join(SUPPORTED_LANGUAGES)}."
        )
    return langs


def pytest_generate_tests(metafunc):
    if "sdk_language" in metafunc.fixturenames:
        langs = _selected_languages()
        metafunc.parametrize("sdk_language", langs, scope="module", ids=lambda v: v)

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


@pytest.fixture(scope='module')
def get_template_id():
    """Resolve a template id to use for ``test_get_template``.

    Resolution order:
      1. ``TEMPLATE_ID`` env var (explicit override).
      2. First template returned by ``/v3/template/list`` for the
         configured API key.
      3. ``None`` — the test should skip in this case.
    """
    override = os.environ.get('TEMPLATE_ID')
    if override:
        print(f"\nUsing TEMPLATE_ID override :: {override}")
        return override

    try:
        res = helpers_hsapi.get_list_templates(page_size=30)
    except Exception as exc:  # network / DNS / auth header issues
        print(f"\nCould not list templates: {exc!r}")
        return None

    if res.status_code != 200:
        print(f"\ntemplate/list returned {res.status_code}: {res.text[:500]}")
        return None

    try:
        res_json = json.loads(res.text)
    except json.JSONDecodeError:
        return None

    templates = res_json.get('templates') or []
    if not templates:
        return None

    template_id = templates[0].get('template_id')
    print(f"\nResolved Template ID :: {template_id}")
    return template_id
    # for app_num in range(len(res_json['api_apps'])):
    #     if res_json['api_apps'][app_num]['name'] == HS_API_APP:
    #         # Get the client_id
    #         print(f"App Name found ::  {res_json['api_apps'][app_num]['name']}")
    #         client_id = res_json['api_apps'][app_num]['client_id']
    #         print(f"Client ID :: {client_id}")
    #         return client_id






