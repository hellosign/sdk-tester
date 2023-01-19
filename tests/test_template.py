import pytest
import os
import sys
import json
from pathlib import Path
scriptdir = os.path.dirname(os.path.realpath(__file__))
utilsdir = f'{scriptdir}/utils/'
sys.path.insert(0, utilsdir)
import helpers_hsapi
import shared_records

root_dir = os.path.abspath(os.curdir)
print(f"root dir {root_dir}")

def test_get_template(container_bin,sdk_language,uploads_dir,auth_type,auth_key,server,get_clientid):
    getTemplate_filename = f'{root_dir}/test_fixtures/template/getTemplate.json'
    with open(getTemplate_filename) as json_file:
        json_decoded = json.load(json_file)
    templateid =''
    if server == 'api.qa-hellosign.com':
        templateid = shared_records.qa_bulk_send_template_id
    elif server == 'api.staging-hellosign.com':
        templateid = shared_records.staging_bulk_send_template_id
    elif server == 'api.hellosign.com':
        templateid = shared_records.prod_template_id

    #Append client_id into JSON.
    #json_decoded["data"]["client_id"] = get_clientid
    #print(f"template id {shared_records.template_id}")
    json_decoded["parameters"]["template_id"] = templateid
    # This step is to covert the JSON into duoble quotes. ptherwise we get error `Expecting property name enclosed in double quotes`
    json_decoded = json.dumps(json_decoded)
    print(f"json decoded {json_decoded}")
    response = helpers_hsapi.run(json_decoded, container_bin, sdk_language, uploads_dir, auth_type,
                                 auth_key, server)

    print(f"\n\nResponse : test_get_template {response.body}")
    assert response.status_code == 200