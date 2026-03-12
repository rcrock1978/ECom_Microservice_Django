from pathlib import Path


def read_readme() -> str:
    data = Path("README.md").read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "utf-16"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise AssertionError("Unable to decode README.md")


def test_quickstart_mentions_verified_startup_and_seed_flow() -> None:
    content = read_readme()

    assert "docker compose up -d --build" in content
    assert "seed_coupons" in content
    assert "seed_products" in content
    assert "Architecture Summary" in content
