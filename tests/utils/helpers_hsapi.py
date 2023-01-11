
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
    # json_dump = json.dumps(payload)
    print(f"typeof {type(json_dump)}")
    print(f"json_dump {json_dump}")
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
            # f'--json={get_clientid}'
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


def base64encoding(api_key):
    base64_bytes = api_key.encode("ascii")
    message_bytes = base64.b64encode(base64_bytes)
    decoded = message_bytes.decode("ascii")
    return decoded


def get_list_api_apps(auth_type, auth_key, server, page_size=30):
    """ List the API apps """
    print(f"server {server}")
    env = 'staging-hellosign'
    api_key = 'a966bff49f99ced8314eb714aced5fca0441928f4eb362baad31730fa0dc31f4' + ':'
    apikey = base64encoding(api_key)
    hsapi_list_api_apps = Template('https://api.$env.com/v3/api_app/list?page_size=$page_size')
    url = hsapi_list_api_apps.substitute(env=env, page_size=page_size)

    print(f"Auth type {auth_type}")
    print(f"auth key {api_key}")
    headers = {
        'Authorization': 'Basic ' + apikey,
    }

    print(f"\n URL %s {url}")
    res = None
    res = requests.get(url, headers=headers)

    print(f"\n Response : get_api_app: {res.status_code}")


    return res