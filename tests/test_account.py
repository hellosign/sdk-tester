import uuid


def test_create_account_success(sdk_runner, sdk_retry_runner):
    email_address = f'signer-{uuid.uuid4().hex}@example.com'
    create_response = sdk_runner(
        "account/accountCreate.json",
        {"email_address": email_address},
        expected_status=200,
    )
    assert create_response.body['account']['email_address'] == email_address

    verify_response = sdk_runner(
        "account/accountVerify.json",
        {"email_address": email_address},
        expected_status=200,
    )
    assert verify_response.body['account']['email_address'] == email_address


def test_get_account(sdk_runner):
    response = sdk_runner(
        "account/accountGet.json",
        expected_status=200,
    )
    assert response.body['account']['account_id']
    assert response.body['account']['email_address']


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
