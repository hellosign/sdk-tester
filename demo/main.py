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
            uploads_dir: str,
            auth_type: str,
            auth_key: str,
            server: str,
    ):
        self._container_bin = container_bin
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
            f'-u{self._uploads_dir}',
            f'-a{self._auth_type}',
            f'-k{self._auth_key}',
            f'-s{self._server}',
            f'-j{base64_json_string}',
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

    # One of "node", "php", "python". Coming soon: "ruby", "csharp", "java"
    sdk_language = 'php'
    # Uploads directory, containing PDFs you may want to upload to the API
    uploads_dir = f'{dir_path}/uploads_dir'
    # One of "apikey" or "oauth"
    api_auth = 'apikey'
    # The API key or OAuth bearer token to use for the request
    api_key = 'fef31706c2825a4d08c27987031f0aaaff7b9f298d2e926233b834183dc6a872'
    # Change server, ie dev/qa/staging/prod
    server = 'api.dev-hellosign.com'

    container_bin = f'{dir_path}/openapi-integration-tests/{sdk_language}-run'

    tester = ApiTester(
        container_bin,
        uploads_dir,
        api_auth,
        api_key,
        server,
    )

    test_create_account_success(tester)
    test_create_account_failure(tester)
