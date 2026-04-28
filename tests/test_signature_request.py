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
