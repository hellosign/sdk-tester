import base64
import json
import os
import subprocess
import uuid
from typing import NamedTuple


class ApiResponse(NamedTuple):
    body: dict
    status_code: int
    headers: dict


class ApiTester(object):
    def __init__(
            self,
            container_bin: str,
            sdk_language: str,
            uploads_dir: str,
            auth_type: str,
            auth_key: str,
            server: str,
    ):
        self._container_bin = container_bin
        self._sdk_language = sdk_language
        self._uploads_dir = uploads_dir
        self._auth_type = auth_type
        self._auth_key = auth_key
        self._server = server

    def run(self, payload: dict) -> ApiResponse:
        json_dump = json.dumps(payload)
        base64_json = base64.b64encode(json_dump.encode('utf-8'))
        base64_json_string = base64_json.decode('utf-8')

        cmd = [
            self._container_bin,
            f'--sdk={self._sdk_language}',
            f'--auth_type={self._auth_type}',
            f'--auth_key={self._auth_key}',
            f'--uploads_dir={self._uploads_dir}',
            f'--server={self._server}',
            f'--json={base64_json_string}',
        ]
        response = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if response.returncode:
            raise RuntimeError(
                "Error running container:\n" +
                response.stdout.decode('utf-8')
            )

        if response.stderr:
            raise RuntimeError(
                "Error running container:\n" +
                response.stderr.decode('utf-8')
            )

        payload = json.loads(response.stdout.decode('utf-8'))

        return ApiResponse(
            body=payload['body'],
            status_code=payload['status_code'],
            headers=payload['headers'],
        )


def test_create_account_success(tester: ApiTester):
    email_address = f'signer{uuid.uuid4()}@example.com'

    json_data = {
        "operationId": "accountCreate",
        "parameters": {},
        "data": {
            "email_address": email_address,
        },
        "files": {},
    }

    response = tester.run(json_data)

    assert response.status_code == 200
    assert response.body['account']['email_address'] == email_address


def test_create_account_failure(tester: ApiTester):
    email_address = 'INVALID_EMAIL_ADDRESS@.com'

    json_data = {
        "operationId": "accountCreate",
        "parameters": {},
        "data": {
            "email_address": email_address,
        },
        "files": {},
    }

    response = tester.run(json_data)

    assert response.status_code == 400
    assert 'email_address not valid' in response.body['error']['error_msg']


if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))

    #
    # Grab the following from config file, environment, or somewhere else
    #

    # One of "node", "php", "python", "ruby", "csharp", "java"
    sdk_language = 'php'
    # Uploads directory, containing PDFs you may want to upload to the API
    uploads_dir = f'{dir_path}/../file_uploads'
    # One of "apikey" or "oauth"
    api_auth = 'apikey'
    # The API key or OAuth bearer token to use for the request
    api_key = os.environ['API_KEY']
    # Change server, ie dev/qa/staging/prod
    server = 'api.hellosign.com'

    container_bin = f'{dir_path}/../run'

    tester = ApiTester(
        container_bin,
        sdk_language,
        uploads_dir,
        api_auth,
        api_key,
        server,
    )

    test_create_account_success(tester)
    test_create_account_failure(tester)
