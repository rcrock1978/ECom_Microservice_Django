from pathlib import Path


def read_readme() -> str:
    data = Path("README.md").read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "utf-16"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise AssertionError("Unable to decode README.md")


def test_coupon_validation_and_reward_credit_thresholds_documented() -> None:
    content = read_readme()

    assert "SC-009" in content
    assert "coupon validation <1s" in content
    assert "SC-010" in content
    assert "reward credit <30s" in content
