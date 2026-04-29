
import json
import os
import re
import subprocess
import time
import uuid
from typing import NamedTuple
import requests
from string import Template, ascii_lowercase, digits
import base64

_FIXTURES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fixtures'))
_PLACEHOLDER_RE = re.compile(r'\{\{(\w+)\}\}')


def load_fixture(fixture_path, placeholders=None):
    """Load a fixture JSON file, replace ``{{placeholder}}`` tokens, return a JSON string.

    Parameters
    ----------
    fixture_path : str
        Path relative to ``tests/fixtures/``,
        e.g. ``"signature_request/signatureRequestSend.json"``.
    placeholders : dict[str, str] | None
        Mapping of placeholder names to runtime values.
    """
    placeholders = placeholders or {}
    full_path = os.path.join(_FIXTURES_DIR, fixture_path)

    with open(full_path) as f:
        content = f.read()

    for name, value in placeholders.items():
        content = content.replace('{{' + name + '}}', str(value))

    remaining = _PLACEHOLDER_RE.findall(content)
    if remaining:
        raise ValueError(
            f"Unfilled placeholders in {fixture_path}: {', '.join(sorted(set(remaining)))}. "
            f"Pass them in the placeholders dict."
        )

    json.loads(content)
    return content


class ApiResponse(NamedTuple):
    body: dict
    status_code: int
    headers: dict


def _invoke(cmd):
    """Run the container harness once and return the parsed ApiResponse.

    - Non-zero exit code is treated as an infrastructure failure; both stdout
      and stderr are surfaced so the caller can debug.
    - Stderr on a zero exit is treated as non-fatal noise (e.g. the
      ``WARNING: The requested image's platform (linux/amd64) does not match
      the detected host platform`` message emitted by Docker Desktop on ARM
      Macs when running an amd64-only image).
    - If stdout cannot be parsed as JSON the caller gets both streams back
      so the real error is visible instead of an empty RuntimeError.
    """
    completed = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout = completed.stdout.decode('utf-8', errors='replace')
    stderr = completed.stderr.decode('utf-8', errors='replace')

    if completed.returncode:
        raise RuntimeError(
            "Error running container (exit {}):\nstdout:\n{}\nstderr:\n{}".format(
                completed.returncode, stdout, stderr,
            )
        )

    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Container stdout was not valid JSON: {}\nstdout:\n{}\nstderr:\n{}".format(
                exc, stdout, stderr,
            )
        ) from exc

    return ApiResponse(
        body=payload['body'],
        status_code=payload['status_code'],
        headers=payload['headers'],
    )


def run(json_dump, container_bin, sdk_language, uploads_dir, auth_type, auth_key, server):
    base64_json = base64.b64encode(json_dump.encode('utf-8'))
    base64_json_string = base64_json.decode('utf-8')

    cmd = [
        container_bin,
        f'--sdk={sdk_language}',
        f'--auth_type={auth_type}',
        f'--auth_key={auth_key}',
        f'--uploads_dir={uploads_dir}',
        f'--server={server}',
        f'--json={base64_json_string}',
    ]

    max_retries = int(os.environ.get('SDK_TESTER_RATE_LIMIT_RETRIES', '3'))
    default_backoff_seconds = float(
        os.environ.get('SDK_TESTER_RATE_LIMIT_BACKOFF', '7'),
    )

    attempt = 0
    while True:
        response = _invoke(cmd)
        if response.status_code != 429 or attempt >= max_retries:
            return response

        attempt += 1
        backoff = _rate_limit_backoff(response.headers, default_backoff_seconds)
        print(
            f"Got 429 from API (attempt {attempt}/{max_retries}); "
            f"sleeping {backoff:.1f}s before retry..."
        )
        time.sleep(backoff)


def _rate_limit_backoff(headers, default_seconds):
    """Honour the API's rate-limit hints when we get back a 429.

    Header names come back in mixed case depending on the SDK in use
    (Java capitalises them, most others lowercase them), so match
    case-insensitively. Values may also be wrapped in a list by the Java
    response shape.
    """
    def _get(name):
        for key, value in (headers or {}).items():
            if key.lower() == name.lower():
                return value[0] if isinstance(value, list) else value
        return None

    retry_after = _get('Retry-After')
    if retry_after:
        try:
            return max(float(retry_after), 1.0)
        except (TypeError, ValueError):
            pass

    reset = _get('X-Ratelimit-Reset')
    if reset:
        try:
            wait = float(reset) - time.time()
            if wait > 0:
                return min(wait + 1.0, 60.0)
        except (TypeError, ValueError):
            pass

    return default_seconds


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