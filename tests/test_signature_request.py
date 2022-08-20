import sys
import json
import base64
import pytest
import os
from pathlib import Path

scriptdir = os.path.dirname(os.path.realpath(__file__))
utilsdir = f'{scriptdir}/utils/'
sys.path.insert(0, utilsdir)
import helpers_hsapi

root_dir = os.path.abspath(os.curdir)
print(f"root dir {root_dir}")

signatureRequestSend_filename = f'{root_dir}/test_fixtures/signatureRequestSend-example_01.json'
with open(signatureRequestSend_filename, "r") as fs:
    signatureRequestSend_data = fs.read()


def test_signature_request_send(container_bin, sdk_language, uploads_dir, auth_type, auth_key, server):
    # json_data = {
    #         "operationId": "signatureRequestSend",
    #         "parameters": {},
    #         "data": {
    #             "cc_email_addresses": [
    #                 "hs-api-qa+sdk+cc1@hellosign.com",
    #                 "hs-api-qa+sdk+cc2@hellosign.com"
    #             ],
    #             "message": "Please sign this NDA and then we can discuss more. Let me know if you\nhave any questions.",
    #             "signers": [
    #                 {
    #                     "email_address": "hs-api-qa+sdk+signer@hellosign.com",
    #                     "name": "Signer 1",
    #                     "order": 0,
    #                     "sms_phone_number": "+14155550100",
    #                     "sms_phone_number_type": "delivery"
    #                 }
    #             ],
    #             "subject": "The NDA we talked about",
    #             "test_mode": False,
    #             "title": "NDA with Acme Co."
    #         },
    #         "files": {
    #             "file": [
    #                 "pdf-sample.pdf",
    #                 "pdf-sample-2.pdf",
    #             ]
    #         }
    #     }

    # json_dump = json.dumps(json_data)
    # #print(f"json_dump {json_dump}")

    response = helpers_hsapi.run(signatureRequestSend_data, container_bin, sdk_language, uploads_dir, auth_type,
                                 auth_key, server)

    print(f"\n\nResponse : test_signature_request_send {response.body}")
    assert response.status_code == 200


signatureRequestCreateEmbedded_filename = f'{root_dir}/test_fixtures/signatureRequestCreateEmbedded.json'
with open(signatureRequestCreateEmbedded_filename, "r") as fs:
    signatureRequestCreateEmbedded_data = fs.read()


def test_signature_request_create_embedded(container_bin, sdk_language, uploads_dir, auth_type, auth_key, server):
    # print(f"sdk langauage {sdk_language}")
    # print(f"url {server}")
    # json_data = {
    #         "operationId":"signatureRequestCreateEmbedded",
    #         "data": {
    #         "allow_decline": True,
    #         "allow_reassign": True,
    #         "attachments": [
    #             {
    #                 "name": "Attachment1",
    #                 "signer_index": 1,
    #                 "instructions": "Upload your Driver's License",
    #                 "required": True
    #             }
    #         ],
    #         "cc_email_addresses": [
    #             "hs-api-qa+sdk+cc1@hellosign.com",
    #             "hs-api-qa+sdk+cc2@hellosign.com"
    #         ],
    #         "client_id": "bf1bcf9ccedc24f9e23e7358af0348b0",
    #         "custom_fields": [
    #             {
    #                 "name": "Cost",
    #                 "value": "$20,000",
    #                 "editor": "Client",
    #                 "required": True
    #             }
    #         ],
    #         "field_options": {
    #             "date_format": "MM / DD / YYYY"
    #         },
    #         "file": [
    #             "pdf-sample.pdf"
    #         ],
    #         "form_field_groups": {"checkbox_group_1":{"group_label":"group","requirement":"require_1"},
    #                               "radio_group_1":{"group_label":"group","requirement":"require_1"}},
    #
    #         "form_field_rules":
    #         [{"id":"rule_0","trigger_operator":"AND","triggers":[{"id":"text_1","operator":"is","value":"foo"}],"actions":[{"field_id":"text_2","hidden":1,"type":"change-field-visibility"}]}],
    #         "form_fields_per_document": [
    #             {"document_index": 0,"api_id": "checkbox_1", "name": "checkbox_field_name_1", "height": 100, "required": 1, "signer": 0,
    #              "width": 100, "x": 50, "y": 50, "type": "checkbox"},
    #             {"document_index": 0,"api_id": "checkbox_2", "name": "checkbox_field_name_2", "height": 100, "signer": 0, "width": 100,
    #              "x": 250, "y": 50, "type": "checkbox", "group": "checkbox_group_1"},
    #             {"document_index": 0,"api_id": "checkbox_3", "name": "checkbox_field_name_3", "height": 100, "signer": 0, "width": 100,
    #              "x": 450, "y": 50, "type": "checkbox", "group": "checkbox_group_1"},
    #             {"document_index": 0,"api_id": "dropdown_1", "name": "dropdown_field_name_3", "height": 100, "required": 1, "signer": 0,
    #              "width": 100, "x": 50, "y": 250, "options": ["Option 1", "Option 2"], "type": "dropdown"},
    #             {"document_index": 0,"api_id": "radio_1", "name": "radio_field_name_1", "height": 100, "signer": 0, "width": 100, "x": 50,
    #              "y": 450, "type": "radio", "group": "radio_group_1"},
    #             {"document_index": 0,"api_id": "radio_2", "name": "radio_field_name_2", "height": 100, "signer": 0, "width": 100, "x": 250,
    #              "y": 450, "type": "radio", "group": "radio_group_1"},
    #             {"document_index": 0,"api_id": "text_1", "name": "text_field_name_1", "height": 100, "required": 1, "signer": 0,
    #              "width": 100, "x": 50, "y": 650, "type": "text"},
    #             {"document_index": 0,"api_id": "text_2", "name": "text_field_name_2", "height": 100, "required": 1, "signer": 0,
    #              "width": 100, "x": 250, "y": 650, "type": "text"},
    #             {"document_index": 0,"api_id": "text_3", "name": "text_field_name_3", "height": 100, "required": 1, "signer": 0,
    #              "width": 100, "x": 450, "y": 650, "type": "text"},
    #             {"document_index": 0,"api_id": "text_4", "name": "text_field_name_4", "height": 100, "required": 1, "signer": 0,
    #              "width": 100, "x": 650, "y": 650, "type": "text"}
    #         ],
    #         "hide_text_tags": False,
    #         "message": "Please sign this NDA and then we can discuss more. Let me know if you have any questions.",
    #         "metadata": {
    #             "field1": "value1"
    #         },
    #         "signers": [
    #             {
    #                 "email_address": "hs-api-qa+sdk+signer1@hellosign.com",
    #                 "name": "Jack",
    #                 "order": 0
    #             },
    #             {
    #                 "email_address": "hs-api-qa+sdk+signer2@hellosign.com",
    #                 "name": "Jill",
    #                 "order": 1
    #             }
    #         ],
    #         "signing_options": {
    #             "draw": True,
    #             "type": True,
    #             "upload": True,
    #             "phone": False,
    #             "default_type": "draw"
    #         },
    #         "subject": "The NDA we talked about",
    #         "test_mode": True,
    #         "title": "NDA with Acme Co.",
    #         "use_text_tags": False
    #      }
    # }

    # json_data = {
    #                 "operationId":"signatureRequestCreateEmbedded",
    #                 "data": {
    #                 "allow_decline": True,
    #                 "allow_reassign": True,
    #                 "attachments": [
    #                     {
    #                         "name": "Attachment1",
    #                         "signer_index": 1,
    #                         "instructions": "Upload your Driver's License",
    #                         "required": True
    #                     }
    #                 ],
    #                 "cc_email_addresses": [
    #                     "hs-api-qa+sdk+cc1@hellosign.com",
    #                     "hs-api-qa+sdk+cc2@hellosign.com"
    #                 ],
    #                 "client_id": "bf1bcf9ccedc24f9e23e7358af0348b0",
    #                 "custom_fields": [
    #                     {
    #                         "name": "Cost",
    #                         "value": "$20,000",
    #                         "editor": "0",
    #                         "required": True
    #                     }
    #                 ],
    #                 "field_options": {
    #                     "date_format": "MM / DD / YYYY"
    #                 },
    #                 "form_field_rules": [
    #                     {
    #                         "id": "rule_1",
    #                         "trigger_operator": "AND",
    #                         "triggers": [
    #                             {
    #                                 "id": "uniqueIdHere_1",
    #                                 "operator": "is",
    #                                 "value": "foo"
    #                             }
    #                         ],
    #                         "actions": [
    #                             {
    #                                 "field_id": "uniqueIdHere_2",
    #                                 "hidden": True,
    #                                 "type": "change-field-visibility"
    #                             }
    #                         ]
    #                     }
    #                 ],
    #                 "form_fields_per_document": [
    #                     {
    #                         "document_index": 0,
    #                         "api_id": "uniqueIdHere_1",
    #                         "name": "",
    #                         "type": "text",
    #                         "x": 112,
    #                         "y": 328,
    #                         "width": 100,
    #                         "height": 16,
    #                         "required": True,
    #                         "signer": "0",
    #                         "page": 1,
    #                         "validation_type": "numbers_only",
    #                     },
    #                     {
    #                         "document_index": 0,
    #                         "api_id": "uniqueIdHere_2",
    #                         "name": "",
    #                         "type": "signature",
    #                         "x": 530,
    #                         "y": 415,
    #                         "width": 120,
    #                         "height": 30,
    #                         "required": True,
    #                         "signer": "0",
    #                         "page": 1,
    #                     },
    #                     {
    #                         "document_index": 0,
    #                         "api_id": "uniqueIdHere_3",
    #                         "name": "",
    #                         "type": "signature",
    #                         "x": 789,
    #                         "y": 567,
    #                         "width": 120,
    #                         "height": 30,
    #                         "required": True,
    #                         "signer": "1",
    #                         "page": 1,
    #                     }
    #                 ],
    #                 "hide_text_tags": False,
    #                 "message": "Please sign this NDA and then we can discuss more. Let me know if you have any questions.",
    #                 "metadata": {
    #                     "field1": "value1"
    #                 },
    #                 "signers": [
    #                     {
    #                         "email_address": "hs-api-qa+sdk+signer1@hellosign.com",
    #                         "name": "Jack",
    #                         "order": 0
    #                     },
    #                     {
    #                         "email_address": "hs-api-qa+sdk+signer2@hellosign.com",
    #                         "name": "Jill",
    #                         "order": 1
    #                     }
    #                 ],
    #                 "signing_options": {
    #                     "draw": True,
    #                     "type": True,
    #                     "upload": True,
    #                     "phone": False,
    #                     "default_type": "draw"
    #                 },
    #                 "subject": "The NDA we talked about",
    #                 "test_mode": True,
    #                 "title": "NDA with Acme Co.",
    #                 "use_text_tags": False
    #              },
    #              "files": {
    #                  "file": [
    #                    "pdf-sample.pdf"
    #                  ]
    #              },
    #              "parameters": {}
    #         }

    response = helpers_hsapi.run(signatureRequestCreateEmbedded_data, container_bin, sdk_language, uploads_dir,
                                 auth_type, auth_key, server)

    print(f"\n\nResponse : test_signature_request_create_embedded {response.body}")
    assert response.status_code == 200
