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
    uploads_dir = f'{dir_path}/tests/file_uploads'
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
    """Resolve an API-app ``client_id`` for tests that need one.

    Resolution order:
      1. ``CLIENT_ID`` env var (explicit override).
      2. First API app returned by ``/v3/api_app/list`` for the
         configured API key.
      3. ``None`` — the caller should skip in this case.
    """
    override = os.environ.get('CLIENT_ID')
    if override:
        print(f"\nUsing CLIENT_ID override :: {override}")
        return override

    try:
        res = helpers_hsapi.get_list_api_apps(page_size=30)
    except Exception as exc:
        print(f"\nCould not list api apps: {exc!r}")
        return None

    if res.status_code != 200:
        print(f"\napi_app/list returned {res.status_code}: {res.text[:500]}")
        return None

    try:
        res_json = json.loads(res.text)
    except json.JSONDecodeError:
        return None

    api_apps = res_json.get('api_apps') or []
    if not api_apps:
        return None

    client_id = api_apps[0].get('client_id')
    print(f"\nResolved Client ID :: {client_id}")
    return client_id


def _resolve_json(fixture_or_data, placeholders):
    if isinstance(fixture_or_data, dict):
        return json.dumps(fixture_or_data)
    elif isinstance(fixture_or_data, str) and fixture_or_data.endswith('.json'):
        return helpers_hsapi.load_fixture(fixture_or_data, placeholders)
    return fixture_or_data

@pytest.fixture
def sdk_runner(container_bin, sdk_language, uploads_dir, auth_type, auth_key, server):
    def _run(fixture_or_data, placeholders=None, expected_status=None):
        json_str = _resolve_json(fixture_or_data, placeholders)

        response = helpers_hsapi.run(
            json_str, container_bin, sdk_language, uploads_dir,
            auth_type, auth_key, server,
        )

        if expected_status is not None:
            assert response.status_code == expected_status, (
                f"Expected {expected_status}, got {response.status_code}: {response.body}"
            )

        return response

    return _run

@pytest.fixture
def sdk_retry_runner(container_bin, sdk_language, uploads_dir, auth_type, auth_key, server):
    def _run(fixture_or_data, placeholders=None, expected_status=200, retries=5, retry_wait=2):
        import time
        json_str = _resolve_json(fixture_or_data, placeholders)

        for attempt in range(retries):
            response = helpers_hsapi.run(
                json_str, container_bin, sdk_language, uploads_dir,
                auth_type, auth_key, server,
            )
            if response.status_code == expected_status:
                return response
            if attempt < retries - 1:
                time.sleep(retry_wait)

        assert response.status_code == expected_status, (
            f"Expected {expected_status} after {retries} attempts, got {response.status_code}: {response.body}"
        )
        return response

    return _run
