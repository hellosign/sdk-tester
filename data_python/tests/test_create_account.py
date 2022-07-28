import json
import os
import base64
import subprocess
import unittest

def test_create_account(
    container: str,
    auth_method: str,
    api_auth: str,
    server: str,
):
    json_data = {
        "operationId": "accountCreate",
        "parameters": {},
        "data": {
            "email_address": "njanapareddy+01@dropbox.com"
        },
        "files": {}
    }

    json_dump = json.dumps(json_data)
    base64_json = base64.b64encode(json_dump.encode('utf-8'))
    base64_json_string = base64_json.decode('utf-8')

    dir_path = os.path.dirname(os.path.realpath(__file__))

    cmd = [
        f'{dir_path}/../../{container}-run',
        f'-a{auth_method}',
        f'-k{api_auth}',
        f'-s{server}',
        f'-j{base64_json_string}',
    ]
    response = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    json_response = json.loads(response.stdout.decode('utf-8'))
    print(f'JSON Response :: {json_response}')

if __name__ == '__main__':
    test_create_account(
        'python',
        'apikey',
        '6d45ee28ddcb38733d6a484a06a2dda68c2c21eb18bb10ece9b54aea2727ff6b',
        'api.qa-hellosign.com',
    )