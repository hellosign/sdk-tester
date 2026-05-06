# sdk-tester

Language-agnostic harness that exercises the Dropbox Sign OpenAPI SDKs. Each
supported SDK lives inside a dedicated Docker image; the `./run` script feeds
a normalised JSON payload to the image and returns a normalised JSON response,
which makes it easy to drive the same scenario through every SDK from a single
test suite.

Supported SDKs: `dotnet`, `java`, `node`, `php`, `python`, `ruby` (`csharp` is
accepted as an alias for `dotnet`).

See `[./demo](./demo)` for an example of how to embed the harness in your own
test code.

## Quickstart

```bash
# 1. Build all SDK images (or just the ones you care about, e.g. ./build python)
./build all

# 2. Point at production and drop in a Dropbox Sign API key tied to a
#    test account. Keep tests in test_mode (see "Safety" below).
export API_KEY="YOUR_DROPBOX_SIGN_API_KEY"
export SERVER="api.hellosign.com"

# 3. Run the pytest suite against one SDK...
LANGUAGE=python pytest -svra tests/

# ...or fan the same tests out across every SDK in one go
LANGUAGES=python,node,php,ruby,java,dotnet pytest -svra tests/
```

Firing a single request (no pytest) instead:

```bash
./run \
    --sdk=python \
    --auth_type=apikey \
    --auth_key="$API_KEY" \
    --server=api.hellosign.com \
    --json="${PWD}/tests/fixtures/accounts/accountCreate-example_01.json"
```

> **Safety**: the harness talks to the real Dropbox Sign API. Use an API key
> bound to a dedicated test account, and keep `test_mode: true` in payloads
> that create signature requests or unclaimed drafts. Rotate the key if it
> ever lands in shell history, CI logs, or a screenshot.

## Environment variables

The pytest suite and helper utilities read the following variables. `./run`
itself only takes CLI flags — it does not read env vars.

Variables are automatically loaded from `.env.staging` via
[pytest-dotenv](https://pypi.org/project/pytest-dotenv/) (configured in
`pytest.ini`). To use a different env file, override the `env_files` option:

```bash
# Use a custom env file
pytest --override-ini="env_files=.env.production" -svra tests/
```

A typical `.env.staging` looks like:

```dotenv
API_KEY=your_api_key_here
SERVER=api.hellosign.com
LANGUAGES=python,node
CLIENT_ID=your_client_id
```

All `.env.*` files are gitignored — credentials stay local.


| Variable                          | Scope        | Required | Default | Meaning                                                                                                                                  |
| --------------------------------- | ------------ | -------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `API_KEY`                         | pytest       | yes      | —       | Dropbox Sign API key used for every request issued by the suite.                                                                         |
| `SERVER`                          | pytest       | yes      | —       | API host (no scheme). Production is `api.hellosign.com`.                                                                                 |
| `LANGUAGES`                       | pytest       | yes\*    | —       | Comma-separated list of SDKs to exercise, e.g. `python,node`. Turns `pytest tests/` into a matrix run.                                   |
| `LANGUAGE`                        | pytest       | yes\*    | —       | Single SDK; kept for backwards compatibility. Set exactly one of `LANGUAGES` / `LANGUAGE`.                                               |
| `CLIENT_ID`                       | pytest       | no       | —       | API-App `client_id` for embedded / unclaimed-draft tests. When unset the fixture uses the first app returned by `/v3/api_app/list`.     |
| `SDK_TESTER_RATE_LIMIT_RETRIES`   | pytest       | no       | `3`     | How many times `helpers_hsapi.run` retries on HTTP 429 before giving up.                                                                 |
| `SDK_TESTER_RATE_LIMIT_BACKOFF`   | pytest       | no       | `7`     | Fallback backoff in seconds when the API does not return `Retry-After` / `X-Ratelimit-Reset`.                                            |

\* Either `LANGUAGES` or `LANGUAGE` must be set. `conftest.py` fails loudly
rather than defaulting to an arbitrary SDK.

## Prerequisites

- Docker (Docker Desktop, Colima, OrbStack, etc.) running locally.
- Bash (any version — the scripts no longer rely on Bash 4-only syntax).
- Python 3 with `pytest` + `requests`, if you want to run the pytest suite:
  ```bash
  pip3 install pytest requests
  ```

## Building the SDK containers

`./build` produces one Docker image per SDK (`dropbox/sign-<sdk>:latest`).

```text
./build [options] SDK
```

Options:


| Flag            | Meaning                                                                                                                                                                                    |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `--sdk-ref REF` | Git ref (branch/tag/commit) for SDKs sourced from git (`python`, `ruby`, `node`, `dotnet`). For `java` this is the Maven Central version (defaults to the latest `<release>` published on Maven Central). For `php` it is the Composer version constraint. |
| `--local PATH`  | Build against a local SDK source directory instead of fetching it from git / a package registry. Mutually exclusive with `all`.                                                            |
| `--help`        | Show help and exit.                                                                                                                                                                        |


`SDK` is one of `dotnet java node php python ruby` or `all` (or `csharp` as an
alias for `dotnet`). Examples:

```bash
./build all                          # build every SDK from defaults
./build python                       # build just python
./build --sdk-ref=v1.4.0 node        # pin node to a specific upstream ref
./build --sdk-ref=2.6.0 java         # pin java to a specific Maven Central release
./build --local ../dropbox-sign-python python   # build against a local SDK
```

### Where each SDK comes from


| SDK    | Default source                                                              | Definition file                |
| ------ | --------------------------------------------------------------------------- | ------------------------------ |
| python | `github.com/hellosign/dropbox-sign-python @ main`                           | `adapters/python/requirements.txt` |
| ruby   | `github.com/hellosign/dropbox-sign-ruby @ main`                             | `adapters/ruby/Gemfile`            |
| node   | `github:hellosign/dropbox-sign-node#main`                                   | `adapters/node/package.json`       |
| dotnet | `github.com/hellosign/dropbox-sign-dotnet @ main` (cloned inside the image) | `adapters/dotnet/Dockerfile`       |
| php    | Packagist `dropbox/sign ^1.0.0`                                             | `adapters/php/composer.json`       |
| java   | Maven Central `com.dropbox.sign:dropbox-sign` (latest `<release>`)          | `adapters/java/pom.xml`            |


`--sdk-ref` rewrites the relevant descriptor in a staged build context (under
`.build-ctx/<sdk>/`, git-ignored) so the originals in `adapters/<sdk>/` are never
touched. `--local` does the same plus copies your local SDK into the context
at `./sdk-src/` and rewrites the descriptor to reference `/sdk-src` inside the
container (for Java it `mvn install`s the local SDK into the image-local Maven
repo and pins the tester's `pom.xml` to the version in the local `pom.xml`).

For Java, `./build java` with no `--sdk-ref` fetches
`https://repo1.maven.org/maven2/com/dropbox/sign/dropbox-sign/maven-metadata.xml`
and pins the staged `pom.xml` to the `<release>` value it reports — so the
default tracks "latest published Maven Central release" the same way the git
based SDKs track `main`. If that fetch fails (offline, Maven Central outage)
the build falls back to the `<version>` baked into `adapters/java/pom.xml` and
prints a warning.

### How `./build` runs the SDK

`./build` always runs with `--no-cache`. If your local SDK tree has a large
`node_modules/`, `vendor/`, `target/`, `build/`, `dist/`, `bin/`, `obj/`,
`venv/`, `.venv/`, `__pycache__/`, or `*.egg-info/` folder, it is excluded from
the copy so the build context stays small.

## Running a single request with `./run`

```text
./run [options]
```


| Flag                   | Required | Description                                                                                  |
| ---------------------- | -------- | -------------------------------------------------------------------------------------------- |
| `--sdk=<sdk>`          | yes      | `dotnet`, `java`, `node`, `php`, `python`, `ruby` (or `csharp`).                             |
| `--auth_type=<type>`   | yes      | `apikey` or `oauth`.                                                                         |
| `--auth_key=<value>`   | yes      | API key (for `apikey`) or OAuth bearer token (for `oauth`).                                  |
| `--json=<path or b64>` | yes      | Either a path to a JSON file or a base64-encoded JSON string.                                |
| `--server=<host>`      | no       | API host (no scheme). Defaults to `api.hellosign.com`.                                       |
| `--uploads_dir=<path>` | no       | Directory mounted at `/file_uploads`. Defaults to `./tests/file_uploads`.                          |
| `--dev_mode`           | no       | Mount the local `adapters/<sdk>/requester.*` over the one baked into the image (see note below). |
| `--help`               | no       | Show help and exit.                                                                          |


`./run` mounts `--uploads_dir` at `/file_uploads` in the container; any file
names used under `files` in your JSON payload must live in that directory.

### Run examples

Using a JSON file:

```bash
./run \
    --sdk=php \
    --auth_type=apikey \
    --auth_key=$HS_API_KEY \
    --json="${PWD}/tests/fixtures/accounts/accountCreate-example_01.json"
```

Using a base64-encoded JSON string:

```bash
./run \
    --sdk=node \
    --auth_type=apikey \
    --auth_key=$HS_API_KEY \
    --json="$(printf '{"operationId":"accountCreate","parameters":{},"data":{"email_address":"test_user@example.com"},"files":{}}' | base64)"
```

> Prefer environment variables over pasting secrets on the command line; values
> on the command line are visible in your shell history and in `ps` output.

### `--dev_mode`

`--dev_mode` mounts the local `adapters/<sdk>/requester.*` script over the one
baked into the image so you can iterate on the per-SDK requester code without
rebuilding. It does **not** remount the SDK itself — to iterate on the SDK
source, rebuild the image with `--local`:

```bash
./build --local ../dropbox-sign-python python
```

Dev mode also enables the `XDEBUG_SESSION=xdebug` cookie on outbound requests,
which is handy when debugging the API backend. Edits to the repo-root
`[data.json](./data.json)` (git-ignored) are picked up by dev mode.

## Running the pytest suite

`conftest.py` exposes fixtures the tests under `tests/` consume
(`container_bin`, `sdk_language`, `uploads_dir`, `auth_type`, `auth_key`,
`server`). The first one is a parametrized fixture that lets a single `pytest`
invocation fan out across multiple SDKs.

See [Environment variables](#environment-variables) above for the full list of
variables the suite understands. Auth type is pinned to `apikey` in
`conftest.py`.

### Examples

Run every test against a single SDK:

```bash
LANGUAGE=python \
API_KEY=$HS_API_KEY \
SERVER=api.hellosign.com \
pytest -svra tests/
```

Run every test against every SDK (matrix) in one process:

```bash
LANGUAGES=python,node,php,ruby,java,dotnet \
API_KEY=$HS_API_KEY \
SERVER=api.hellosign.com \
pytest -svra tests/
```

Tests come out as `test_create_account_success[python]`,
`test_create_account_success[node]`, etc. Filter a subset with `-k`:

```bash
LANGUAGES=python,node,php,ruby,java,dotnet \
API_KEY=$HS_API_KEY \
SERVER=api.hellosign.com \
pytest -svra tests/test_account.py -k "python or node"
```

Run a single test on a single SDK:

```bash
LANGUAGE=python \
API_KEY=$HS_API_KEY \
SERVER=api.hellosign.com \
pytest -svra tests/test_signature_request.py::test_signature_request_send
```

Run the matrix with per-SDK reports in parallel processes (`&` + `wait`), one
pytest per SDK:

```bash
for lang in python node php ruby java dotnet; do
    LANGUAGE=$lang API_KEY=$HS_API_KEY SERVER=api.hellosign.com \
        pytest -svra tests/ --junitxml=reports/${lang}.xml &
done
wait
```

> Tests hit the real API. Use an API key bound to a dedicated test account
> and keep payloads that create signature requests or unclaimed drafts in
> `test_mode: true` so real documents are never dispatched.

## JSON payload shape

The `--json` file (or base64 blob) passed to `./run` must conform to:

```json
{
    "operationId": "<string>",
    "data": {},
    "parameters": {},
    "files": {}
}
```

### `operationId` (required)

Must match an `operationId` in the
[OpenAPI spec's `paths` object](https://github.com/hellosign/hellosign-openapi/blob/oas-release/openapi.yaml).
For example:

```yaml
paths:
  /account/create:
    post:
      tags: [Account]
      summary: 'Create Account'
      operationId: accountCreate
```

### `data`

Request body. Must be an object (may be empty).

### `parameters`

Query / path parameters. For example, `GET /account` takes an `account_id`
query parameter.

### `files`

Files to upload, if the endpoint supports them. Every filename must live in
`--uploads_dir` (default `./tests/file_uploads`). For endpoints that accept several
files, use a nested array:

```json
"files": { "files": ["pdf-sample.pdf", "pdf-sample-2.pdf"] }
```

### JSON payload examples

Get an account (query parameter, no body):

```json
{
    "operationId": "accountGet",
    "parameters": { "account_id": "test_account_id" },
    "data": {},
    "files": {}
}
```

Create an API App with a file upload:

```json
{
    "operationId": "apiAppCreate",
    "parameters": {},
    "data": {
        "name": "My Production App",
        "callback_url": "https://example.com/callback",
        "domains": ["example.com"],
        "oauth": {
            "callback_url": "https://example.com/oauth",
            "scopes": ["basic_account_info", "request_signature"]
        }
    },
    "files": { "custom_logo_file": "pdf-sample.pdf" }
}
```

Send a signature request with multiple file uploads:

```json
{
    "operationId": "signatureRequestSend",
    "parameters": {},
    "data": {
        "cc_email_addresses": ["test_user@example.com"],
        "signers": [
            {
                "email_address": "test_user@example.com",
                "name": "Test Signer",
                "order": 0
            }
        ],
        "subject": "The NDA we talked about",
        "test_mode": true,
        "title": "NDA with Acme Co."
    },
    "files": { "files": ["pdf-sample.pdf", "pdf-sample-2.pdf"] }
}
```

More examples live under `[./tests/fixtures](./tests/fixtures)`.

## Response shape

Every response — success or error — comes back as:

```json
{
    "body": {},
    "status_code": 0,
    "headers": {}
}
```

Header names are always lowercased. A successful response looks like:

```json
{
    "body": {
        "account": {
            "account_id": "test_account_id",
            "email_address": "test_user@example.com",
            "is_locked": false,
            "is_paid_hs": false,
            "is_paid_hf": false,
            "quotas": { "api_signature_requests_left": 0, "documents_left": 3, "templates_left": 0 },
            "locale": "en-US"
        }
    },
    "status_code": 200,
    "headers": { "content-type": "application/json" }
}
```

An error response looks like:

```json
{
    "body": {
        "error": { "error_msg": "Unauthorized api key", "error_name": "unauthorized" }
    },
    "status_code": 401,
    "headers": { "content-type": "application/json" }
}
```

## Troubleshooting

- `**${SELECTED_SDK,,}: bad substitution**` — the scripts used Bash 4 syntax
that macOS's system Bash 3.2 does not support. The current `./build` uses
portable `tr` instead; pull the latest version if you see this.
- **Node image build fails on axios `.d.ts`** — TypeScript is too old. The
image now uses TypeScript 5.x with `skipLibCheck: true` to insulate against
third-party typing churn.
- **Java image build fails with `com.github.hellosign:dropbox-sign-java:main-SNAPSHOT`
not found** — the harness now pulls the published `com.dropbox.sign:dropbox-sign`
artifact from Maven Central rather than JitPack. By default `./build java`
auto-resolves the latest `<release>` from `maven-metadata.xml`; to pin a
specific version pass `./build --sdk-ref=<version> java`.
- **Java build prints `could not resolve latest Java version from Maven
Central`** — the `maven-metadata.xml` fetch failed (offline, DNS, proxy).
The build falls back to the `<version>` pinned in `adapters/java/pom.xml`; if
that is too old, re-run with an explicit `--sdk-ref=<version> java` once the
network is back.
- **.NET build complains about incompatible target framework** — the upstream
SDK targets `net8.0`; the image uses `mcr.microsoft.com/dotnet/sdk:8.0`. If
upstream bumps its target, bump the base image in `adapters/dotnet/Dockerfile`.
- `**LANGUAGES` / `LANGUAGE` missing** — `conftest.py` now fails loudly rather
than defaulting to an arbitrary SDK. Set one of them before running pytest.

## License

Unless otherwise noted:

```text
Copyright (c) 2023 Dropbox, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

