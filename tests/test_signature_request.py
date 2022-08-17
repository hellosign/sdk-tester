import sys

from main import *

dir_path = os.path.dirname(os.path.realpath(__file__))
print(f"dir path {dir_path}")

container_bin = f'{dir_path}/../run'
    #
    # Grab the following from config file, environment, or somewhere else
    #

    # One of "node", "php", "python". Coming soon: "ruby", "csharp", "java"
sdk_language = 'php'
    # Uploads directory, containing PDFs you may want to upload to the API
uploads_dir = f'{dir_path}/../file_uploads'
    # One of "apikey" or "oauth"
api_auth = 'apikey'
    # The API key or OAuth bearer token to use for the request
api_key = 'e6b771a5db23aa466b599c928368f9bb9b967bf0ba7d9c58ab194921a3388815'
    # Change server, ie dev/qa/staging/prod
server = 'api.qa-hellosign.com'

def test_signature_request_send(tester: ApiTester):
    json_data = {
        "operationId": "signatureRequestSend",
        "parameters": {},
        "data": {
            "cc_email_addresses": [
                "hs-api-qa+sdk+cc1@hellosign.com",
                "hs-api-qa+sdk+cc2@hellosign.com"
            ],
            "message": "Please sign this NDA and then we can discuss more. Let me know if you\nhave any questions.",
            "signers": [
                {
                    "email_address": "hs-api-qa+sdk+signer@hellosign.com",
                    "name": "Signer 1",
                    "order": 0,
                    "sms_phone_number": "+14155550100",
                    "sms_phone_number_type": "delivery"
                }
            ],
            "subject": "The NDA we talked about",
            "test_mode": False,
            "title": "NDA with Acme Co."
        },
        "files": {
            "file": [
                "pdf-sample.pdf",
                "pdf-sample-2.pdf",
            ]
        }
    }
    response = tester.run(json_data)

    print(f"\n\nResponse : test_signature_request_send {response.body}")
    assert response.status_code == 200


def test_signature_request_create_embedded(tester: ApiTester):
    print(f"sdk langauage {sdk_language}")
    print(f"url {server}")
    json_data = {
        "default": {
            "allow_decline": True,
            "allow_reassign": True,
            "attachments": [
                {
                    "name": "Attachment1",
                    "signer_index": 1,
                    "instructions": "Upload your Driver's License",
                    "required": True
                }
            ],
            "cc_email_addresses": [
                "hs-api-qa+sdk+cc1@hellosign.com",
                "hs-api-qa+sdk+cc2@hellosign.com"
            ],
            "client_id": "c534d49b9399e1de6eeb493fc184ee06",
            "custom_fields": [
                {
                    "name": "Cost",
                    "value": "$20,000",
                    "editor": "Client",
                    "required": True
                }
            ],
            "field_options": {
                "date_format": "MM / DD / YYYY"
            },
            "file": [
                "pdf-sample.pdf"
            ],
            "form_field_groups": [
                {
                    "group_id": "RadioGroup1",
                    "group_label": "Radio Group 1",
                    "requirement": "require_0-1"
                }
            ],
            "form_field_rules": [
                {
                    "id": "rule_1",
                    "trigger_operator": "AND",
                    "triggers": [
                        {
                            "id": "uniqueIdHere_1",
                            "operator": "is",
                            "value": "foo"
                        }
                    ],
                    "actions": [
                        {
                            "field_id": "uniqueIdHere_2",
                            "hidden": True,
                            "type": "change-field-visibility"
                        }
                    ]
                }
            ],
            "form_fields_per_document": [
                {
                    "document_index": 0,
                    "api_id": "uniqueIdHere_1",
                    "name": "",
                    "type": "text",
                    "x": 112,
                    "y": 328,
                    "width": 100,
                    "height": 16,
                    "required": True,
                    "signer": "0",
                    "page": 1,
                    "validation_type": "numbers_only"
                },
                {
                    "document_index": 0,
                    "api_id": "uniqueIdHere_2",
                    "name": "",
                    "type": "signature",
                    "x": 530,
                    "y": 415,
                    "width": 120,
                    "height": 30,
                    "required": True,
                    "signer": "0",
                    "page": 1
                }
            ],
            "hide_text_tags": False,
            "message": "Please sign this NDA and then we can discuss more. Let me know if you have any questions.",
            "metadata": {
                "field1": "value1"
            },
            "signers": [
                {
                    "email_address": "hs-api-qa+sdk+signer1@hellosign.com",
                    "name": "Jack",
                    "order": 0
                },
                {
                    "email_address": "hs-api-qa+sdk+signer2@hellosign.com",
                    "name": "Jill",
                    "order": 1
                }
            ],
            "signing_options": {
                "draw": True,
                "type": True,
                "upload": True,
                "phone": False,
                "default_type": "draw"
            },
            "subject": "The NDA we talked about",
            "test_mode": True,
            "title": "NDA with Acme Co.",
            "use_text_tags": False
        }
    }

    response = tester.run(json_data)
    print(f"\n\nResponse : test_signature_request_create_embedded {response.body}")
    assert response.status_code == 200


tester = ApiTester(
    container_bin,
    sdk_language,
    uploads_dir,
    api_auth,
    api_key,
    server,
)

#test_signature_request_send(tester)
test_signature_request_create_embedded(tester)