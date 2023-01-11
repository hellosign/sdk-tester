import sys
import json
import base64
import pytest
import os
from pathlib import Path

scriptdir = os.path.dirname(os.path.realpath(__file__))
utilsdir = f'{scriptdir}/tests/utils/'
print(f"utils dir {utilsdir}")
sys.path.insert(0, utilsdir)
import helpers_hsapi

root_dir = os.path.abspath(os.curdir)
print(f"root dir {root_dir}")

signatureRequestSend_filename = f'{root_dir}/test_fixtures/signatureRequestSend-example_01.json'
# with open(signatureRequestSend_filename, "r") as fs:
#     signatureRequestSend_data = fs.read()


def test_signature_request_send(container_bin, sdk_language, uploads_dir, auth_type, auth_key, server,get_clientid):
    with open(signatureRequestSend_filename) as json_file:
        json_decoded = json.load(json_file)

    json_decoded['client_id'] = get_clientid

    json_decoded = str(json_decoded)

    # with open(signatureRequestSend_filename, 'w') as json_file:
    #     json.dump(json_decoded, json_file)
    #
    # with open(signatureRequestSend_filename, "r") as fs:
    #     signatureRequestSend_data = fs.read()

    print(f"signatureRequestSend_data {json_decoded}")
    response = helpers_hsapi.run(json_decoded, container_bin, sdk_language, uploads_dir, auth_type,
                                 auth_key, server)

    print(f"\n\nResponse : test_signature_request_send {response.body}")
    assert response.status_code == 200


signatureRequestCreateEmbedded_filename = f'{root_dir}/test_fixtures/signatureRequestCreateEmbedded.json'
with open(signatureRequestCreateEmbedded_filename, "r") as fs:
    signatureRequestCreateEmbedded_data = fs.read()


def test_signature_request_create_embedded(container_bin, sdk_language, uploads_dir, auth_type, auth_key, server):
    response = helpers_hsapi.run(signatureRequestCreateEmbedded_data, container_bin, sdk_language, uploads_dir,
                                 auth_type, auth_key, server)

    print(f"\n\nResponse : test_signature_request_create_embedded {response.body}")
    assert response.status_code == 200
