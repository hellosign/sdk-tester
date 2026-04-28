import uuid


def test_create_account_success(sdk_runner):
    email_address = f'signer-{uuid.uuid4().hex}@example.com'
    response = sdk_runner(
        "account/accountCreate.json",
        {"email_address": email_address},
        expected_status=200,
    )
    assert response.body['account']['email_address'] == email_address


def test_create_account_failure(sdk_runner):
    response = sdk_runner(
        "account/accountCreate.json",
        {"email_address": "INVALID_EMAIL_ADDRESS@.com"},
        expected_status=400,
    )
    error = response.body.get('error', {})
    assert error.get('error_name') == 'bad_request', (
        f"Expected a bad_request error for an invalid email, got {response.body!r}"
    )
