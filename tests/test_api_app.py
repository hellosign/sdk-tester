import uuid


def test_api_app_lifecycle(sdk_runner, sdk_retry_runner):
    # 1. Create API app
    app_name = f'Test App {uuid.uuid4().hex[:8]}'
    create_response = sdk_runner(
        "api_app/apiAppCreate.json",
        {"app_name": app_name},
        expected_status=201,
    )
    client_id = create_response.body['api_app']['client_id']
    assert create_response.body['api_app']['name'] == app_name

    # 2. Get API app
    get_response = sdk_retry_runner(
        "api_app/apiAppGet.json",
        {"client_id": client_id},
    )
    assert get_response.body['api_app']['client_id'] == client_id
    assert get_response.body['api_app']['name'] == app_name

    # 3. List API apps - should contain the created app
    list_response = sdk_runner(
        "api_app/apiAppList.json",
        expected_status=200,
    )
    app_ids = [app['client_id'] for app in list_response.body['api_apps']]
    assert client_id in app_ids

    # 4. Update API app
    updated_name = f'Updated App {uuid.uuid4().hex[:8]}'
    update_response = sdk_runner(
        "api_app/apiAppUpdate.json",
        {"client_id": client_id, "app_name": updated_name},
        expected_status=200,
    )
    assert update_response.body['api_app']['name'] == updated_name

    # 5. Delete API app
    sdk_runner(
        "api_app/apiAppDelete.json",
        {"client_id": client_id},
        expected_status=204,
    )
