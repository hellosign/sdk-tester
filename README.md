# About

This project aims to allow making an API request using any of our
supported OpenAPI SDKs.

# Demo

See [./demo](./demo) for a demo
on how this project may be used in our testing suite.

# How to Use

## Generate Container Image

Each SDK will have its own container image. These are appended with `-build`.
You can run the SDK's  corresponding build script to generate an image locally.

For PHP SDK:

```bash
./php-build
```

For Python SDK:

```bash
./python-build
```

For Node SDK:

```bash
./node-build
```

## Run Tool

Each SDK will have its own run script. These are appended with `-run`.

Example:

```bash
$ ./php-run

Uses the HelloSign PHP SDK to make a request to the HelloSign API
-a          Auth type, one of "apikey" or "oauth"
-k          Auth key.
            If -a=apikey, pass API Key.
            If -a=oauth, pass OAuth Bearer Token.
-s          The server to use, must be like "api.hellosign.com"
-f          A valid JSON file containing all request data
-j          A base64-encoded JSON string. Replaces -f
-u          Directory where files that can be uploaded to the API live.
            Defaults to this repo's "file_uploads" directory
-d          Run container in dev mode
-h          display this help and exit
```

The command to run each script is identical to each other, and they all require
the same flags to function correctly.

# Flags

## `-a` Auth Type

Currently we support API key `apikey` or OAuth bearer token `oauth`

## `-k` Auth Key

If auth type (`-a`) is `apikey` this will be the API Key.

If auth type (`-a`) is `oauth` this will be the OAuth bearer token.

## `-s` Server

What server to make the API request to. For example, `api.hellosign.com`.

## `-f` JSON Payload - File

A local file containing the JSON data sent in the request to the API.

Cannot be used with `-j` below.

See the [JSON Data](#json-data) section for more information.

## `-j` JSON Payload - Base64-encoded String

A base64-encoded string containing the JSON data sent in the request to the API.

Cannot be used with `-f` above.

See the [JSON Data](#json-data) section for more information.

## `-u` Uploads Directory

Local directory containing any files you would want to upload in the API request.

Defaults to [./file_uploads](./file_uploads).

## `-d` Dev Mode

Runs the container in dev mode. Simply calling `-d` enabled Dev mode, there is
no need to pass a value to it. It is disabled by default.

Dev mode adds a cookie `XDEBUG_SESSION=xdebug` to the request that allows
debugging the API backend.

It also loads the local `requester.*` file into the container, overwriting the
file that was baked into the image during the build step.

Dev mode is extremely useful when you want to debug the request via the API
backend, or want to make changes to the `requester.*` file locally and test them
out without needing to rebuild the container image.

Using Dev mode you can also change request data (sent to the API) by editing the
[data.json](./data.json) file that is generated after running a build script.
Changes to this file are ignored by git.

# JSON Data

Whether using a local file or a base64-encoded string for the JSON payload
it must match the following shape:

```
{
    "operationId": <string> (required),
    "data": <object>,
    "parameters": <object>,
    "files": <object>
}
```

## `operationId` (Required)

This is a string that must match one of the `operationId` values within the
[OpenAPI spec's `paths` object](https://github.com/hellosign/hellosign-openapi/blob/oas-release/openapi.yaml).

In the example below, the `operationId` value is `accountCreate`:

```yaml
paths:
  /account/create:
    post:
      tags:
        - Account
      summary: 'Create Account'
      description: 'Creates a new HelloSign Account that is associated with the specified `email_address`.'
      operationId: accountCreate
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AccountCreateRequest'
            examples:
              default_example:
                $ref: '#/components/examples/AccountCreateRequestDefaultExample'
              oauth:
                $ref: '#/components/examples/AccountCreateRequestOAuthExample'
```

## `data`

The data to be sent to the API in the body of the request. Must be an object.

## `parameters`

If the API endpoint you want to use has query parameters, you must define them here.

For example, `GET /account` has a `account_id` query parameter.

## `files`

If the API endpoint you want to use allows uploading files, you must define them here.

The file you want to use _must_ be found in the `test_assets` directory!

If the endpoint supports multiple files you must pass a nested object.

## JSON Examples

### `accountGet` (with parameters)

```json
{
  "operationId": "accountGet",
  "parameters": {
    "account_id": "5d38f3a287c072a2ac741191c5c055936a56b933"
  },
  "data": {},
  "files": {}
}
```

### `apiAppCreate` (single file upload)

```json
{
  "operationId": "apiAppCreate",
  "parameters": {},
  "data": {
    "name": "My Production App",
    "callback_url": "https://example.com/callback",
    "domains": [
      "example.com"
    ],
    "oauth": {
      "callback_url": "https://example.com/oauth",
      "scopes": [
        "basic_account_info",
        "request_signature"
      ]
    },
    "options": {
      "can_insert_everywhere": true
    },
    "white_labeling_options": {
      "header_background_color": "#1A1A1A",
      "legal_version": "terms1",
      "link_color": "#00B3E6",
      "page_background_color": "#F7F8F9",
      "primary_button_color": "#00b3e6",
      "primary_button_color_hover": "#00B3E6",
      "primary_button_text_color": "#ffffff",
      "primary_button_text_color_hover": "#FFFFFF",
      "secondary_button_color": "#FFFFFF",
      "secondary_button_color_hover": "#FFFFFF",
      "secondary_button_text_color": "#00B3E6",
      "secondary_button_text_color_hover": "#00B3E6",
      "text_color1": "#808080",
      "text_color2": "#FFFFFF"
    }
  },
  "files": {
    "custom_logo_file": "pdf-sample.pdf"
  }
}
```

### `signatureRequestSend` (multiple file uploads)

```json
{
  "operationId": "signatureRequestSend",
  "parameters": {},
  "data": {
    "cc_email_addresses": [
      "lawyer@hellosign.com",
      "lawyer@example.com"
    ],
    "message": "Please sign this NDA and then we can discuss more. Let me know if you\nhave any questions.",
    "signers": [
      {
        "email_address": "s1@example.com",
        "name": "Signer 1",
        "order": 0,
        "sms_phone_number": "+14155550100",
        "sms_phone_number_type": "delivery"
      }
    ],
    "subject": "The NDA we talked about",
    "test_mode": true,
    "title": "NDA with Acme Co."
  },
  "files": {
    "file": [
      "pdf-sample.pdf",
      "pdf-sample-2.pdf"
    ]
  }
}
```

# Response Examples

All responses will match the following shape, whether the response was
successful or resulted in an error:

```
{
    "body": <object>,
    "status_code": <integer>,
    "headers": <object>
}
```

## Response Success Example

This is an example of a _successful_ API response:

```json
{
    "body": {
        "account": {
            "account_id": "0f7cfef800c571173e5fec744bce8b27c3f30569",
            "email_address": "signer2@hellosign.com",
            "is_locked": false,
            "is_paid_hs": false,
            "is_paid_hf": false,
            "quotas": {
                "api_signature_requests_left": 0,
                "documents_left": 3,
                "templates_left": 0
            },
            "locale": "en-US"
        }
    },
    "status_code": 200,
    "headers": {
        "date": "Tue, 26 Jul 2022 15:16:17 GMT",
        "server": "Apache",
        "x-powered-by": "PHP\/7.4.28",
        "x-robots-tag": "noindex",
        "x-ratelimit-limit": "10000",
        "x-ratelimit-limit-remaining": "9999",
        "x-ratelimit-reset": "1658848577",
        "access-control-allow-origin": "*",
        "access-control-allow-headers": "Authorization, Origin, X-Requested-With, Content-Type, Accept",
        "access-control-allow-methods": "GET, POST, OPTIONS",
        "user-agent": "HelloSign API",
        "vary": "Accept-Encoding",
        "strict-transport-security": "max-age=15768000",
        "p3p": "CP=\"NOP3PPOLICY\"",
        "content-length": "360",
        "connection": "close",
        "content-type": "application\/json"
    }
}
```

Note that header names are all lowercased!

## Response Error Example

This is an example of a _unsuccessful_ API response:

```json
{
    "body": {
        "error": {
            "error_msg": "Unauthorized api key",
            "error_name": "unauthorized"
        }
    },
    "status_code": 401,
    "headers": {
        "date": "Tue, 26 Jul 2022 15:23:38 GMT",
        "content-type": "application\/json",
        "content-length": "74",
        "connection": "keep-alive",
        "server": "Apache",
        "strict-transport-security": "max-age=31536000",
        "vary": "Origin",
        "x-robots-tag": "noindex",
        "access-control-allow-origin": "*",
        "access-control-allow-headers": "Authorization, Origin, X-Requested-With, Content-Type, Accept, Request-URL, Referrer-Policy, Referer, Sec-CH-UA, Sec-CH-UA-Mobile, Sec-CH-UA-Platform, Sec-Fetch-Site, User-Agent, X-User-Agent",
        "access-control-allow-methods": "GET, POST, OPTIONS, PUT, DELETE",
        "user_agent": "HelloSign API",
        "p3p": "CP=\"NOP3PPOLICY\""
    }
}
```

Note that header names are all lowercased!

# Run Examples

The following are some examples with all required flags.

## Example Using Local JSON File

```bash
./php-run \
    -a apikey \
    -k 4e0a8a8bd9fea228a1de515a43a75ded2e495471b830069cc8e1821c13c31ce4 \
    -s "api.hellosign.com" \
    -f "$PWD/test_fixtures/accountCreate-example_01.json"
```

## Example Using Base64-Encoded JSON String

```bash
./node-run \
    -a apikey \
    -k 4e0a8a8bd9fea228a1de515a43a75ded2e495471b830069cc8e1821c13c31ce4 \
    -s "api.hellosign.com" \
    -j "ewogICJvcGVyYXRpb25JZCI6ICJhY2NvdW50Q3JlYXRlIiwKICAicGFyYW1ldGVycyI6IHt9LAogICJkYXRhIjogewogICAgImVtYWlsX2FkZHJlc3MiOiAic2lnbmVyMUBoZWxsb3NpZ24uY29tIgogIH0sCiAgImZpbGVzIjoge30KfQo="
```
