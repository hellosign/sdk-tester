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


unclaimed_draft_create_embedded_filename = f'{root_dir}/test_fixtures/unclaimed_draft/unclaimedDraftCreateEmbedded.json'
with open(unclaimed_draft_create_embedded_filename, "r") as fs:
    unclaimed_draft_create_embedded_data = fs.read()

def test_post_unclaimed_draft_create_embedded(container_bin, sdk_language, uploads_dir, auth_type, auth_key, server):
    response = helpers_hsapi.run(unclaimed_draft_create_embedded_data, container_bin, sdk_language, uploads_dir, auth_type,
                                 auth_key, server)

    print(f"\n\nResponse : test_post_unclaimed_draft_create_embedded {response.body}")
    assert response.status_code == 200




unclaimed_draft_create_embedded_filename = f'{root_dir}/test_fixtures/unclaimed_draft/unclaimedDraftCreateEmbeddedSelfSign.json'
with open(unclaimed_draft_create_embedded_filename, "r") as fs:
    unclaimed_draft_create_embedded__data = fs.read()

def test_post_unclaimed_draft_create_embedded_selfsign(container_bin, sdk_language, uploads_dir, auth_type, auth_key, server):
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
    response = helpers_hsapi.run(unclaimed_draft_create_embedded__data, container_bin, sdk_language, uploads_dir, auth_type,
                                 auth_key, server)

    print(f"\n\nResponse : test_post_unclaimed_draft_create_embedded {response.body}")
    assert response.status_code == 200




# def write_json(new_data, filename='createEmbedded.json'):
#     with open(filename, 'r+') as file:
#         # First we load existing data into a dict.
#         file_data = json.load(file)
#         # Join new_data with file_data inside emp_details
#         file_data["data"]["default"]["client_id"] = 'dbsdjfasdfnasdkfjadskfjasdkfads'
#         # Sets file's current position at offset.
#         file.seek(0)
#         # convert back to json.
#         json.dump(file_data, file, indent=4)
#
#     # python object to be appended


 # unclaimed_draft_create_embedded_filename = f'{root_dir}/test_fixtures/unclaimed_draft/unclaimedDraftCreateEmbedded.json'
    # with open(unclaimed_draft_create_embedded_filename, "r+") as fs:
    #     # First we load existing data into a dict.
    #     file_data = json.load(fs)
    #     # Join new_data with file_data inside file_data["data"]["default"]
    #     #file_data["data"]["default"]["client_id"] = get_client_id
    #     # Sets file's current position at offset.
    #     fs.seek(0)
    #     # convert back to json.
    #     json.dump(file_data, fs, indent=4)
    #     unclaimed_draft_create_embedded_data = fs.read()
    #     print(f"unclaimed_draft_create_embedded_data {file_data}\n")
    # payload = json.dumps(unclaimed_draft_create_embedded__data)
    # print(f"payload  {payload}\n\n")
    # payload["data"]["client_id"] = get_client_id
    # print(f"payload with client_id {payload}\n\n")


# unclaimed_draft_create_embedded_filename = f'{root_dir}/test_fixtures/unclaimed_draft/unclaimedDraftCreateEmbedded.json'
# with open(unclaimed_draft_create_embedded_filename, "r+") as fs:
#     # First we load existing data into a dict.
#     file_data = json.load(fs)
#     # Join new_data with file_data inside file_data["data"]["default"]
#     #file_data["data"]["default"]["client_id"] = get_client_id
#     # Sets file's current position at offset.
#     fs.seek(0)
#     # convert back to json.
#     json.dump(file_data, fs, indent=4)
#     unclaimed_draft_create_embedded_data = fs.read()
#     print(f"unclaimed_draft_create_embedded_data {file_data}\n")
# payload = json.dumps(unclaimed_draft_create_embedded__data)
# print(f"payload  {payload}\n\n")
# payload["data"]["client_id"] = get_client_id
# print(f"payload with client_id {payload}\n\n")