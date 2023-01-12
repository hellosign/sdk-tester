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

def test_post_unclaimed_draft_create_embedded(container_bin, sdk_language, uploads_dir, auth_type, auth_key, server,get_clientid):
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
    unclaimed_draft_create_embedded_filename = f'{root_dir}/test_fixtures/unclaimed_draft/unclaimedDraftCreateEmbedded.json'
    with open(unclaimed_draft_create_embedded_filename) as json_file:
        json_decoded = json.load(json_file)

    json_decoded["data"]["client_id"] = get_clientid

    json_decoded = json.dumps(json_decoded)
    response = helpers_hsapi.run(json_decoded, container_bin, sdk_language, uploads_dir, auth_type,
                                 auth_key, server)

    print(f"\n\nResponse : test_post_unclaimed_draft_create_embedded {response.body}")
    assert response.status_code == 200





def test_post_unclaimed_draft_create_embedded_selfsign(container_bin, sdk_language, uploads_dir, auth_type, auth_key, server,get_clientid):
    '''
    :param container_bin:
    :param sdk_language:
    :param uploads_dir:
    :param auth_type:
    :param auth_key:
    :param server:
    :param get_client_id:
    :return:
    In JSON - type = "send_document"
    '''
    unclaimed_draft_create_embedded_filename = f'{root_dir}/test_fixtures/unclaimed_draft/unclaimedDraftCreateEmbeddedSelfSign.json'
    with open(unclaimed_draft_create_embedded_filename) as json_file:
        json_decoded = json.load(json_file)

    json_decoded["data"]["client_id"] = get_clientid

    json_decoded = json.dumps(json_decoded)

    response = helpers_hsapi.run(json_decoded, container_bin, sdk_language, uploads_dir, auth_type,
                                 auth_key, server)

    print(f"\n\nResponse : test_post_unclaimed_draft_create_embedded {response.body}")
    assert response.status_code == 200
