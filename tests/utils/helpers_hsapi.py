import requests
def get_list_api_apps(test_instance, get_api_key, api_env_url, page_size=30):
    """ List the API apps """
    if not get_api_key:
        test_instance.fail('ERROR - api_key is required')

    url = shared_records.hsapi_list_api_apps.substitute(env=api_env_url, page_size=page_size)

    headers = {
        'Authorization': 'Basic ' + get_api_key,
    }

    print(f"\n URL %s {url}")

    res = requests.get(url, headers=headers)

    print(f"\n Response : get_api_app: {res.status_code}")

    return res