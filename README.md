# About

This project aims to allow making an API request using any of our
supported OpenAPI SDKs.

# Demo

See [./demo](./demo) for a demo
on how this project may be used in our testing suite.

# How to Use

## Generate Container Images

Each SDK will have its own container image. You can build all containers in one
go by running:

```bash
./build all
```

or build each individually by passing the SDK as parameter:

```bash
# csharp
./build csharp
# java
./build java
# Node
./build node
# PHP
./build php
# Python
./build python
# Ruby
./build ruby
```

## Run Tool

You run any container using the `./run` script and passing the SDK as parameter:

```bash
$ ./run php

Uses the selected HelloSign OpenAPI SDK to make a request to the HelloSign API
--sdk             one of "csharp", "java", "node", "php", "python", "ruby"
                    (required)
--auth_type       one of "apikey", "oauth"
                    (required)
--auth_key        auth key
                    If --auth_key=apikey, pass API Key
                    If --auth_key=oauth, pass OAuth Bearer Token
                    (required)
--json            valid JSON file containing all request data
                    OR base64-encoded JSON string
                    (required)
--server          API server to use, must be like "api.hellosign.com".
                    (defaults to api.hellosign.com)
--uploads_dir     directory where files that can be uploaded to the API live.
                    (defaults to /Users/jtreminio/www/hellosign/openapi/sdk-tester/file_uploads)
--dev_mode        run container in dev mode
                    (optional, default false)
--help            display this help and exit
```

The command to run each script is identical to each other, and they all require
the same flags to function correctly.

# Flags

## `--sdk` SDK (required)

One of `csharp`, `java`, `node`, `php`, `python`, `ruby`.

## `--auth_type` Auth Type (required)

Currently we support API key `apikey` or OAuth bearer token `oauth`

## `--auth_key` Auth Key (required)

If auth type (`--auth_type`) is `apikey` this will be the API Key.

If auth type (`--auth_type`) is `oauth` this will be the OAuth bearer token.

## `--json` JSON Payload (required)

A local file containing the JSON data sent in the request to the API, OR
a base64-encoded string containing the JSON data sent in the request to the API.

See the [JSON Data](#json-data) section for more information.

## `--server` Server (optional)

What server to make the API request to. For example, `api.hellosign.com`.

## `--uploads_dir` Uploads Directory (optional)

Local directory containing any files you would want to upload in the API request.

Defaults to [./file_uploads](./file_uploads).

## `--dev_mode` Dev Mode

Runs the container in dev mode. Simply calling `--dev_mode` enabled Dev mode,
there is  no need to pass a value to it. It is disabled by default.

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

The file you want to use _must_ be found in the [`file_uploads`](./file_uploads) directory!

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
./run \
    --sdk=php \
    --auth_type=apikey \
    --auth_key=4e0a8a8bd9fea228a1de515a43a75ded2e495471b830069cc8e1821c13c31ce4 \
    --json="${PWD}/test_fixtures/accountCreate-example_01.json"
```

## Example Using Base64-Encoded JSON String

```bash
./run \
    --sdk=node \
    --auth_type=apikey \
    --auth_key=4e0a8a8bd9fea228a1de515a43a75ded2e495471b830069cc8e1821c13c31ce4 \
    --json="ewogICJvcGVyYXRpb25JZCI6ICJhY2NvdW50Q3JlYXRlIiwKICAicGFyYW1ldGVycyI6IHt9LAogICJkYXRhIjogewogICAgImVtYWlsX2FkZHJlc3MiOiAic2lnbmVyMUBoZWxsb3NpZ24uY29tIgogIH0sCiAgImZpbGVzIjoge30KfQo="
```
