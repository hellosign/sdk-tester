def test_create_get_and_delete_template(sdk_runner, sdk_retry_runner, get_clientid):
    create_response = sdk_runner(
        "template/templateCreate.json",
        {"client_id": get_clientid},
        expected_status=200,
    )

    template_id = create_response.body['template']['template_id']

    sdk_retry_runner(
        "template/getTemplate.json",
        {"template_id": template_id},
        retry_wait=3,
    )

    # List templates - should contain the created one
    list_response = sdk_runner(
        "template/templateList.json",
        expected_status=200,
    )
    template_ids = [t['template_id'] for t in list_response.body['templates']]
    assert template_id in template_ids

    sdk_runner(
        "template/templateDelete.json",
        {"template_id": template_id},
        expected_status=200,
    )
