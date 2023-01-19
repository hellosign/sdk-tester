
import json
import os
import subprocess
import uuid
from typing import NamedTuple
import requests
from string import Template, ascii_lowercase, digits
import base64

class ApiResponse(NamedTuple):
    body: dict
    status_code: int
    headers: dict


def run(json_dump,container_bin,sdk_language,uploads_dir,auth_type,auth_key,server):
    #print(f"typeof {type(json_dump)}")
    #print(f"json_dump : \n {json_dump}")
    base64_json = base64.b64encode(json_dump.encode('utf-8'))
    base64_json_string = base64_json.decode('utf-8')
    #print(f"base64_json {base64_json_string}")

    cmd = [
            container_bin,
            f'--sdk={sdk_language}',
            f'--auth_type={auth_type}',
            f'--auth_key={auth_key}',
            f'--uploads_dir={uploads_dir}',
            f'--server={server}',
            f'--json={base64_json_string}'
        ]
    response = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
    )
    print(f"Response  : {response}")
    print(f"Response code : {response.returncode}")
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


def base64encoding(api_key):
    base64_bytes = api_key.encode("ascii")
    message_bytes = base64.b64encode(base64_bytes)
    decoded = message_bytes.decode("ascii")
    return decoded


def get_list_api_apps(page_size=30):
    """ List the API apps """
    server = os.environ['SERVER']
    #print(f"server: {server}")
    auth_key = os.environ['API_KEY']
    auth_key = str(auth_key) + ':'
    apikey = base64encoding(auth_key)
    #print(f"API Key: {apikey}")
    url = f'https://{server}/v3/api_app/list?page_size={page_size}'
    headers = {
        'Authorization': f'Basic {apikey}',
    }

    print(f"\n URL %s {url}")
    res = None
    res = requests.get(url, headers=headers)

    print(f"\n Response : get_api_app: {res.status_code}")

    return res