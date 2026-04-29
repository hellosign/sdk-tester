import pytest
import os
import sys
import json
scriptdir = os.path.dirname(os.path.realpath(__file__))
utilsdir = f'{scriptdir}/utils/'
sys.path.insert(0, utilsdir)
import helpers_hsapi

root_dir = os.path.abspath(os.curdir)
print(f"root dir {root_dir}")

def test_get_template(container_bin, sdk_language, uploads_dir, auth_type, auth_key, server, get_template_id):
    getTemplate_filename = f'{root_dir}/test_fixtures/template/getTemplate.json'
    with open(getTemplate_filename) as json_file:
        json_decoded = json.load(json_file)

    if not get_template_id:
        pytest.skip(
            f"No template available for server {server!r}. "
            "Either the API key has no templates, or set TEMPLATE_ID=<id> to override."
        )

    json_decoded["parameters"]["template_id"] = get_template_id
    json_payload = json.dumps(json_decoded)
    print(f"json decoded {json_payload}")
    response = helpers_hsapi.run(json_payload, container_bin, sdk_language, uploads_dir, auth_type,
                                 auth_key, server)

    print(f"\n\nResponse : test_get_template {response.body}")

    if response.status_code == 404:
        error_name = (response.body.get('error') or {}).get('error_name')
        if error_name == 'not_found':
            pytest.skip(
                f"Template {get_template_id!r} does not exist in {server!r}. "
                "Set TEMPLATE_ID to a template available to this API key."
            )

    assert response.status_code == 200