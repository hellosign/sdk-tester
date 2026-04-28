import time


def test_create_and_get_template(sdk_runner, get_clientid):
    create_response = sdk_runner(
        "template/templateCreate.json",
        {"client_id": get_clientid},
        expected_status=200,
    )

    template_id = create_response.body['template']['template_id']

    max_retries = 5
    wait_seconds = 3
    for attempt in range(max_retries):
        get_response = sdk_runner(
            "template/getTemplate.json",
            {"template_id": template_id},
        )
        print(f"\n\nResponse : templateGet (attempt {attempt + 1}) {get_response.body}")
        if get_response.status_code == 200:
            break
        time.sleep(wait_seconds)
    assert get_response.status_code == 200

    sdk_runner(
        "template/templateDelete.json",
        {"template_id": template_id},
        expected_status=200,
    )
