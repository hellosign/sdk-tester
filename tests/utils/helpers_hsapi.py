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


def run(json_dump,container_bin,sdk_language,uploads_dir,auth_type,auth_key,server):
    # json_dump = json.dumps(payload)
    # print(f"json_dump {json_dump}")
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