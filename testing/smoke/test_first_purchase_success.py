from shared.testing.fixtures import first_purchase_success_event


def test_first_purchase_success_fixture_has_required_fields() -> None:
    event = first_purchase_success_event()

    assert event["funnel"] == "first_purchase"
    assert event["step"] == "checkout_success"
    assert event["converted"] is True
