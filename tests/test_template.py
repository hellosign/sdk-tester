import pytest
import os
import sys
from pathlib import Path
scriptdir = os.path.dirname(os.path.realpath(__file__))
utilsdir = f'{scriptdir}/utils/'
sys.path.insert(0, utilsdir)
import helpers_hsapi

root_dir = os.path.abspath(os.curdir)
print(f"root dir {root_dir}")


getTemplate_filename = f'{root_dir}/test_fixtures/getTemplate.json'
with open(getTemplate_filename, "r") as fs:
    getTemplate_data = fs.read()


def test_get_template(container_bin,sdk_language,uploads_dir,auth_type,auth_key,server):
    response = helpers_hsapi.run(getTemplate_data, container_bin, sdk_language, uploads_dir, auth_type,
                                 auth_key, server)

    print(f"\n\nResponse : test_get_template {response.body}")
    assert response.status_code == 200