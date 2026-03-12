from pathlib import Path


def read_readme() -> str:
    data = Path("README.md").read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "utf-16"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise AssertionError("Unable to decode README.md")


def test_catalog_load_thresholds_documented() -> None:
    content = read_readme()

    assert "SC-002" in content
    assert "p95 < 200ms" in content
    assert "1000 concurrent users" in content


def test_search_latency_threshold_documented() -> None:
    content = read_readme()

    assert "SC-003" in content
    assert "95% of search queries <2s" in content
