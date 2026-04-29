def test_signature_request_send(sdk_runner, sdk_retry_runner, get_clientid):
    send_response = sdk_runner(
        "signature_request/signatureRequestSend.json",
        {"client_id": get_clientid},
        expected_status=200,
    )
    signature_request_id = send_response.body['signature_request']['signature_request_id']

    # Get signature request
    get_response = sdk_retry_runner(
        "signature_request/signatureRequestGet.json",
        {"signature_request_id": signature_request_id},
    )
    assert get_response.body['signature_request']['signature_request_id'] == signature_request_id

    # List signature requests - should contain the created one
    list_response = sdk_runner(
        "signature_request/signatureRequestList.json",
        expected_status=200,
    )
    sr_ids = [sr['signature_request_id'] for sr in list_response.body['signature_requests']]
    assert signature_request_id in sr_ids

    # Edit signature request
    edit_response = sdk_runner(
        "signature_request/signatureRequestEdit.json",
        {"signature_request_id": signature_request_id, "client_id": get_clientid},
        expected_status=200,
    )
    assert edit_response.body['signature_request']['subject'] == 'Updated NDA Subject'

def test_signature_request_create_embedded(sdk_runner, get_clientid):
    response = sdk_runner(
        "signature_request/signatureRequestCreateEmbedded.json",
        {"client_id": get_clientid},
        expected_status=200,
    )

    signature_request_id = response.body['signature_request']['signature_request_id']
    signature_id = response.body['signature_request']['signatures'][0]['signature_id']

    # Edit embedded signature request
    edit_response = sdk_runner(
        "signature_request/signatureRequestEditEmbedded.json",
        {"signature_request_id": signature_request_id, "client_id": get_clientid},
        expected_status=200,
    )
    assert edit_response.body['signature_request']['subject'] == 'Updated Embedded NDA Subject'

    # Get embedded sign URL
    sdk_runner(
        "embedded/embeddedSignUrl.json",
        {"signature_id": signature_id},
        expected_status=200,
    )


def test_signature_request_send_with_template(sdk_runner, sdk_retry_runner, get_clientid):
    # Create a template
    create_response = sdk_runner(
        "template/templateCreate.json",
        {"client_id": get_clientid},
        expected_status=200,
    )
    template_id = create_response.body['template']['template_id']

    # Wait for template to be available
    sdk_retry_runner(
        "template/getTemplate.json",
        {"template_id": template_id},
        retry_wait=3,
    )

    # Send signature request with template
    sdk_runner(
        "signature_request/signatureRequestSendWithTemplate.json",
        {"template_id": template_id},
        expected_status=200,
    )

    # Cleanup
    sdk_runner(
        "template/templateDelete.json",
        {"template_id": template_id},
        expected_status=200,
    )


def test_signature_request_create_embedded_with_template(sdk_runner, sdk_retry_runner, get_clientid):
    # Create a template
    create_response = sdk_runner(
        "template/templateCreate.json",
        {"client_id": get_clientid},
        expected_status=200,
    )
    template_id = create_response.body['template']['template_id']

    # Wait for template to be available
    sdk_retry_runner(
        "template/getTemplate.json",
        {"template_id": template_id},
        retry_wait=3,
    )

    # Create embedded signature request with template
    sdk_runner(
        "signature_request/signatureRequestCreateEmbeddedWithTemplate.json",
        {"template_id": template_id, "client_id": get_clientid},
        expected_status=200,
    )

    # Cleanup
    sdk_runner(
        "template/templateDelete.json",
        {"template_id": template_id},
        expected_status=200,
    )
