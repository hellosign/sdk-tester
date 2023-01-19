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


def test_signature_request_send(container_bin, sdk_language, uploads_dir, auth_type, auth_key, server,get_clientid):
    """
    :param container_bin:
    :param sdk_language:
    :param uploads_dir:
    :param auth_type:
    :param auth_key:
    :param server:
    :param get_clientid:
    :return:
    """
    signatureRequestSend_filename = f'{root_dir}/test_fixtures/signature_request/signatureRequestSend-example_01.json'
    with open(signatureRequestSend_filename) as json_file:
        json_decoded = json.load(json_file)

    #Append client_id into JSON.
    json_decoded["data"]["client_id"] = get_clientid

    # This step is to covert the JSON into duoble quotes. ptherwise we get error `Expecting property name enclosed in double quotes`
    json_decoded = json.dumps(json_decoded)

    print(f"signatureRequestSend_data {json_decoded}")
    response = helpers_hsapi.run(json_decoded, container_bin, sdk_language, uploads_dir, auth_type,
                                 auth_key, server)

    print(f"\n\nResponse : test_signature_request_send {response.body}")
    assert response.status_code == 200



def test_signature_request_create_embedded(container_bin, sdk_language, uploads_dir, auth_type, auth_key, server,get_clientid):
    signatureRequestCreateEmbedded_filename = f'{root_dir}/test_fixtures/signature_request/signatureRequestCreateEmbedded.json'
    with open(signatureRequestCreateEmbedded_filename) as json_file:
        json_decoded = json.load(json_file)

    #Append client_id into JSON.
    json_decoded["data"]["client_id"] = get_clientid

    # This step is to covert the JSON into duoble quotes. ptherwise we get error `Expecting property name enclosed in double quotes`
    json_decoded = json.dumps(json_decoded)

    response = helpers_hsapi.run(json_decoded, container_bin, sdk_language, uploads_dir,
                                 auth_type, auth_key, server)

    print(f"\n\nResponse : test_signature_request_create_embedded {response.body}")
    assert response.status_code == 200
