import pytest
import sys
scriptdir = os.path.dirname(os.path.realpath(__file__))
utilsdir = f'{scriptdir}/utils/'
sys.path.insert(0, utilsdir)
import helpers_hsapi
import os
import json
import requests


@pytest.fixture(scope='module')
def get_env():
    return os.environ.get(shared_records.hsenv_var_name, 'qa')


@pytest.fixture(scope='module')
def get_sdk_env_url(get_env):
    if get_env == shared_records.prod_hs_env_str:
        env_url = 'api.hellosign.com'
    elif get_env == shared_records.staging_hs_env_str:
        env_url = 'api.staging-hellosign.com'
    elif get_env == shared_records.qa_hs_env_str:
        env_url = 'api.qa-hellosign.com'
    else:
        pytest.fail(f'\nERROR - unhandled HS environment ({get_env})')

    return env_url


@pytest.fixture(scope='function')
def get_client_id(get_env, test_instance, get_api_key, get_api_env_url):
    API_APP = ""
    if get_env == shared_records.qa_hs_env_str:
        API_APP = shared_records.HS_API_APP_QA
    if get_env == shared_records.staging_hs_env_str:
        API_APP = shared_records.HS_API_APP_STAGING
    if get_env == shared_records.prod_hs_env_str:
        API_APP = shared_records.HS_API_APP_PROD

    print(f"API APP ::  {API_APP}")
    res = helpers_hsapi.get_list_api_apps(test_instance, get_api_key, get_api_env_url, page_size=30)
    res_json = json.loads(res.text)
    assert res.status_code == shared_records.STATUS_OK
    for app_num in range(len(res_json['api_apps'])):
        if res_json['api_apps'][app_num]['name'] == API_APP:
            # Get the client_id
            print(f"App Name found ::  {res_json['api_apps'][app_num]['name']}")
            client_id = res_json['api_apps'][app_num]['client_id']
            print(f"Client ID :: {client_id}")
            return client_id
    return shared_records.client_id
    #shared_records.get_env_var_value(records.settings, shared_records.cred_apicreds, 'client_id')



@pytest.fixture(scope="module")
def get_api_nonencrypt_key(get_api_env_url, get_env):
    """
    Fetch API Key
    Account : hs-api-qa@hellosign.com - Enterprise account.
    """
    if get_env != shared_records.prod_hs_env_str:
        if get_env == shared_records.staging_hs_env_str:
            #guid = records.settings[shared_records.guid]['staging_hs_internal_guid']
            guid = shared_records.staging_hs_internal_guid
        elif get_env == shared_records.qa_hs_env_str:
            #guid = records.settings[shared_records.guid]['qa_hs_internal_guid']
            guid = shared_records.qa_hs_internal_guid
        email_address = shared_records.hsapi_email_name_no_ext
        encoded_email = shared_records.encode_url(email_address)
        url = shared_records.hsapi_get_api_key_url.substitute(env=get_api_env_url, guid=guid,
                                                              email_address=encoded_email)
        res = requests.get(url)
        res_json = json.loads(res.text)
        api_key = res_json['api_key']
        # api_key = shared_records.base64encoding(api_key)
        print(f"get_api_key : {api_key}")
    else:
        api_key = shared_records.prod_api_key
    return api_key