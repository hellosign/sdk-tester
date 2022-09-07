import pytest
import os
import sys
from pathlib import Path
scriptdir = os.path.dirname(os.path.realpath(__file__))
utilsdir = f'{scriptdir}/utils/'
sys.path.insert(0, utilsdir)
import helpers_hsapi
import uuid
root_dir = os.path.abspath(os.curdir)
print(f"root dir {root_dir}")
import json

accountCreate_filename = f'{root_dir}/test_fixtures/accountCreate-example_01.json'
with open(accountCreate_filename, "r") as fs:
    accountCreate_data = fs.read()


def test_create_account_success(container_bin,sdk_language,uploads_dir,auth_type,auth_key,server):
    email_address = f'signer+{uuid.uuid4()}@hellosign.com'
    json_data = {
        "operationId": "accountCreate",
        "parameters": {},
        "data": {
            "email_address": email_address,
        },
        "files": {},
    }
    json_dump = json.dumps(json_data)
    #print(f"json_dump {json_dump}")

    response = helpers_hsapi.run(json_dump, container_bin, sdk_language, uploads_dir, auth_type,
                                 auth_key, server)
    print(f"\n\nResponse : test_create_account_success {response.body}")
    assert response.status_code == 200
    assert response.body['account']['email_address'] == email_address


def test_create_account_failure(container_bin,sdk_language,uploads_dir,auth_type,auth_key,server):
    email_address = 'INVALID_EMAIL_ADDRESS@.com'

    json_data = {
        "operationId": "accountCreate",
        "parameters": {},
        "data": {
            "email_address": email_address,
        },
        "files": {},
    }

    json_dump = json.dumps(json_data)
    print(f"json_dump {json_dump}")
    response = helpers_hsapi.run(json_dump, container_bin, sdk_language, uploads_dir, auth_type,
                                 auth_key, server)
    print(f"\n\nResponse : test_create_account_failure {response}")
    assert response.status_code == 400
    assert 'email_address not valid' in response.body['error']['error_msg']