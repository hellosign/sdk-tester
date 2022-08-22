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
                "Error running container return code:\n" +
                response.stdout.decode('utf-8')
            )

        if response.stderr:
            raise RuntimeError(
                "Error running containe stderr:\n" +
                response.stderr.decode('utf-8')
            )

        payload = json.loads(response.stdout.decode('utf-8'))

        return ApiResponse(
            body=payload['body'],
            status_code=payload['status_code'],
            headers=payload['headers'],
        )


def test_create_account_success(tester: ApiTester):
    email_address = f'signer{uuid.uuid4()}@hellosign.com'

    json_data = {
        "operationId": "accountCreate",
        "parameters": {},
        "data": {
            "email_address": email_address,
        },
        "files": {},
    }

    response = tester.run(json_data)
    print(f"\n\nResponse : test_create_account_success {response}")
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
    print(f"\n\nResponse : test_create_account_failure {response}")
    assert response.status_code == 400
    assert 'email_address not valid' in response.body['error']['error_msg']

def test_signature_request_create_embedded(tester: ApiTester):
    print(f"sdk langauage {sdk_language}")
    print(f"url {server}")
    json_data = {
                    "operationId":"signatureRequestCreateEmbedded",
                    "data": {
                    "allow_decline": True,
                    "allow_reassign": True,
                    "attachments": [
                        {
                            "name": "Attachment1",
                            "signer_index": 1,
                            "instructions": "Upload your Driver's License",
                            "required": True
                        }
                    ],
                    "cc_email_addresses": [
                        "hs-api-qa+sdk+cc1@hellosign.com",
                        "hs-api-qa+sdk+cc2@hellosign.com"
                    ],
                    "client_id": "efdbab0dd86acda1aaa3d56ea3ded8cf",
                    "custom_fields": [
                        {
                            "name": "Cost",
                            "value": "$20,000",
                            "editor": "0",
                            "required": True
                        }
                    ],
                    "field_options": {
                        "date_format": "MM / DD / YYYY"
                    },
                    "form_fields_per_document": [
                        {
                            "document_index": 0,
                            "api_id": "uniqueIdHere_1",
                            "name": "",
                            "type": "text",
                            "x": 112,
                            "y": 328,
                            "width": 100,
                            "height": 16,
                            "required": True,
                            "signer": "0",
                            "page": 1,
                            "validation_type": "numbers_only",
                        }
                    ],
                    "hide_text_tags": False,
                    "message": "Please sign this NDA and then we can discuss more. Let me know if you have any questions.",
                    "metadata": {
                        "field1": "value1"
                    },
                    "signers": [
                        {
                            "email_address": "hs-api-qa+sdk+signer1@hellosign.com",
                            "name": "Jack",
                            "order": 0
                        },
                        {
                            "email_address": "hs-api-qa+sdk+signer2@hellosign.com",
                            "name": "Jill",
                            "order": 1
                        }
                    ],
                    "signing_options": {
                        "draw": True,
                        "type": True,
                        "upload": True,
                        "phone": False,
                        "default_type": "draw"
                    },
                    "subject": "The NDA we talked about",
                    "test_mode": True,
                    "title": "NDA with Acme Co.",
                    "use_text_tags": False
                 },
                 "files": {
                     "file": [
                       "pdf-sample.pdf"
                     ]
                 },
                 "parameters": {}
            }

    response = tester.run(json_data)
    print(f"\n\nResponse : test_signature_request_create_embedded {response.body}")
    assert response.status_code == 200

if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"dir path {dir_path}")
    #
    # Grab the following from config file, environment, or somewhere else
    #

    # One of "node", "php", "python", "ruby", "csharp", "java"
    sdk_language = os.environ['LANGUAGE']
    # Uploads directory, containing PDFs you may want to upload to the API
    uploads_dir = f'{dir_path}/../file_uploads'
    # One of "apikey" or "oauth"
    api_auth = 'apikey'
    # The API key or OAuth bearer token to use for the request
    api_key = os.environ['API_KEY']
    # Change server, ie dev/qa/staging/prod
    server = os.environ['SERVER']

    container_bin = f'{dir_path}/../run'

    tester = ApiTester(
        container_bin,
        sdk_language,
        uploads_dir,
        api_auth,
        api_key,
        server,
    )

    test_signature_request_create_embedded(tester)
    test_create_account_success(tester)
    test_create_account_failure(tester)

