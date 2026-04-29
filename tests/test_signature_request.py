def test_signature_request_send(sdk_runner, get_clientid):
    sdk_runner(
        "signature_request/signatureRequestSend.json",
        {"client_id": get_clientid},
        expected_status=200,
    )

def test_signature_request_create_embedded(sdk_runner, get_clientid):
    response = sdk_runner(
        "signature_request/signatureRequestCreateEmbedded.json",
        {"client_id": get_clientid},
        expected_status=200,
    )

    signature_id = response.body['signature_request']['signatures'][0]['signature_id']
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
