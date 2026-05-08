# SDK Tester

Language-agnostic test harness for Dropbox Sign OpenAPI SDKs. Each SDK runs inside a Docker container; Python pytest drives the tests uniformly across all languages.

## Project structure

```
conftest.py              # pytest fixtures: sdk_runner, get_clientid, etc.
run                      # bash script that invokes SDK containers via docker
build                    # bash script to build SDK Docker images
tests/
  test_*.py              # pytest test files — use sdk_runner fixture
  utils/
    helpers_hsapi.py     # load_fixture(), run() (sends requests to containers), API helpers
  fixtures/              # JSON request templates with {{placeholder}} tokens
    account/             # accountCreate, accountGet, accountVerify
    api_app/             # apiAppCreate, apiAppGet, apiAppList, apiAppUpdate, apiAppDelete
    embedded/            # embeddedSignUrl
    signature_request/   # send, createEmbedded, edit, editEmbedded, get, list, withTemplate variants
    template/            # templateCreate, getTemplate, templateList, templateDelete
    team/                # teamCreate, teamGet, teamInfo, teamMembers, teamSubTeams, teamUpdate, teamAddMember, teamRemoveMember, teamDelete
    unclaimed_draft/     # unclaimedDraftCreateEmbedded, unclaimedDraftCreateEmbeddedSelfSign
adapters/
  dotnet/                # .NET SDK container (Dockerfile + Program.cs)
  java/                  # Java SDK container (Dockerfile + Requester.java)
  node/                  # Node SDK container (Dockerfile + requester.ts)
  php/                   # PHP SDK container (Dockerfile + requester.php)
  python/                # Python SDK container (Dockerfile + requester.py)
  ruby/                  # Ruby SDK container (Dockerfile + requester.rb)
  file_uploads/          # PDF files used as attachments in test requests
COVERAGE.md              # API endpoint coverage checklist (31/73 endpoints)
openapi.yaml             # (gitignored) fetched on demand — see API reference section below
```

## Supported SDKs

`node`, `php`, `python`, `ruby`, `dotnet`, `java`

## Running tests

Env vars are loaded from `.env.staging` (via pytest-dotenv, configured in `pytest.ini`).

```bash
# Build containers first
./build --sdk=python

# Run all tests
python -m pytest tests/ -v

# Run a single test file
python -m pytest tests/test_account.py -v

# Run a single test
pytest -svra tests/test_signature_request.py::test_signature_request_send

# Collect without running (dry-run)
python -m pytest tests/ -v --co

# Build with local SDK source for debugging
./build --local ../dropbox-sign-python python
```

Optional env vars: `CLIENT_ID`, `SDK_TESTER_RATE_LIMIT_RETRIES` (default 3), `SDK_TESTER_RATE_LIMIT_BACKOFF` (default 7s).

## Writing tests

### Fixture files

JSON files in `tests/fixtures/` use `{{placeholder}}` tokens for dynamic values:

```json
{
  "operationId": "signatureRequestSend",
  "data": {
    "client_id": "{{client_id}}",
    ...
  },
  "files": { "files": ["pdf-sample.pdf"] },
  "parameters": {}
}
```

All fixtures follow the shape: `operationId`, `data`, `files`, `parameters`.

### sdk_runner fixture

Tests use the `sdk_runner` pytest fixture (defined in `conftest.py`) which bundles container_bin, sdk_language, uploads_dir, auth_type, auth_key, and server. It accepts:

- **Fixture path** (str ending in `.json`) + placeholders dict — loads from `tests/fixtures/`, replaces `{{tokens}}`
- **Inline dict** — `json.dumps()` it directly
- **Raw JSON string** — passes through as-is

```python
# From fixture with placeholders + expected_status:
def test_signature_request_send(sdk_runner, get_clientid):
    response = sdk_runner(
        "signature_request/signatureRequestSend.json",
        {"client_id": get_clientid},
        expected_status=200,
    )

# With retry (for eventually-consistent resources):
def test_get_template(sdk_retry_runner):
    response = sdk_retry_runner(
        "template/getTemplate.json",
        {"template_id": template_id},
        retry_wait=3,
    )

# From inline dict:
def test_create_account(sdk_runner):
    response = sdk_runner({
        "operationId": "accountCreate",
        "data": {"email_address": "test@example.com"},
        "parameters": {},
        "files": {},
    })
```

### Key pytest fixtures (conftest.py)

| Fixture | Scope | Description |
|---------|-------|-------------|
| `sdk_runner` | function | Callable to load fixture + run against SDK container. Pass `expected_status` to assert. |
| `sdk_retry_runner` | function | Same as `sdk_runner` but retries until `expected_status` (default 200). Configurable `retries` (default 5) and `retry_wait` (default 2s). |
| `get_clientid` | module | Resolves client_id from `CLIENT_ID` env or API |
| `sdk_language` | module | Parametrized across languages from `LANGUAGES` env |
| `container_bin` | module | Path to `./run` script |
| `uploads_dir` | module | Path to `./tests/file_uploads` |
| `auth_type` | function | Fixed to `'apikey'` |
| `auth_key` | function | From `API_KEY` env |
| `server` | function | From `SERVER` env |

### load_fixture (helpers_hsapi.py)

`load_fixture(fixture_path, placeholders)` — loads a JSON file relative to `tests/fixtures/`, replaces `{{placeholder}}` tokens, raises `ValueError` on unfilled placeholders, validates JSON.

## API reference

The OpenAPI spec is the source of truth for operationIds, request schemas, and parameters when creating new fixtures and tests. Fetch the latest before use:

```bash
curl -fsSL -o openapi.yaml https://raw.githubusercontent.com/hellosign/hellosign-openapi/main/openapi-sdk.yaml
```

The file is gitignored so it's always fetched fresh.

## Request/response flow

1. Test calls `sdk_runner()` → `load_fixture()` + `helpers_hsapi.run()`
2. `run()` base64-encodes the JSON, builds a `./run --sdk=... --json=...` command
3. `./run` bash script launches a Docker container for the selected SDK
4. Container requester (e.g. `adapters/python/requester.py`) decodes JSON, calls the SDK method matching `operationId`
5. Container outputs JSON to stdout: `{"body": {...}, "status_code": 200, "headers": {...}}`
6. `run()` parses this into an `ApiResponse` namedtuple, handles 429 retries
