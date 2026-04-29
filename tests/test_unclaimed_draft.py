def test_post_unclaimed_draft_create_embedded(sdk_runner, get_clientid):
    sdk_runner(
        "unclaimed_draft/unclaimedDraftCreateEmbedded.json",
        {"client_id": get_clientid},
        expected_status=200,
    )


def test_post_unclaimed_draft_create_embedded_selfsign(sdk_runner, get_clientid):
    sdk_runner(
        "unclaimed_draft/unclaimedDraftCreateEmbeddedSelfSign.json",
        {"client_id": get_clientid},
        expected_status=200,
    )
