import uuid


def _cleanup_team(sdk_runner):
    """Remove all invited members and delete the team if one exists."""
    get_response = sdk_runner("team/teamGet.json")
    if get_response.status_code != 200:
        return

    team = get_response.body.get('team', {})
    for account in team.get('invited_accounts', []):
        email = account.get('email_address')
        if email:
            sdk_runner(
                "team/teamRemoveMember.json",
                {"email_address": email},
            )

    for account in team.get('accounts', []):
        email = account.get('email_address')
        if email:
            sdk_runner(
                "team/teamRemoveMember.json",
                {"email_address": email},
            )

    sdk_runner("team/teamDelete.json")


def test_team_lifecycle(sdk_runner, sdk_retry_runner):
    # Cleanup any existing team
    _cleanup_team(sdk_runner)

    # 1. Create account
    email_address = f'signer-{uuid.uuid4().hex}@example.com'
    sdk_runner(
        "account/accountCreate.json",
        {"email_address": email_address},
        expected_status=200,
    )

    # 2. Create team
    team_name = f'Test Team {uuid.uuid4().hex[:8]}'
    create_response = sdk_runner(
        "team/teamCreate.json",
        {"team_name": team_name},
        expected_status=200,
    )
    assert create_response.body['team']['name'] == team_name

    # 3. Add member to team
    sdk_runner(
        "team/teamAddMember.json",
        {"email_address": email_address},
        expected_status=200,
    )

    # 4. Get team info
    get_response = sdk_retry_runner(
        "team/teamGet.json",
    )
    assert get_response.body['team']['name'] == team_name
    assert get_response.body['team']['invited_accounts'][0]['email_address'] == email_address

    # 5. Update team name
    updated_name = f'Updated Team {uuid.uuid4().hex[:8]}'
    update_response = sdk_runner(
        "team/teamUpdate.json",
        {"team_name": updated_name},
        expected_status=200,
    )
    assert update_response.body['team']['name'] == updated_name

    # 6. Remove member from team
    sdk_runner(
        "team/teamRemoveMember.json",
        {"email_address": email_address},
        expected_status=200,
    )

    # 7. Delete team
    sdk_runner(
        "team/teamDelete.json",
        expected_status=200,
    )
