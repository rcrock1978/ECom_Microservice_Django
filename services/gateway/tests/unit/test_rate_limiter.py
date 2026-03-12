from gateway.infrastructure.rate_limiter import InMemoryRateLimiter


def test_rate_limiter_allows_within_limit() -> None:
    limiter = InMemoryRateLimiter()
    assert limiter.allow("key-a", 2) is True
    assert limiter.allow("key-a", 2) is True


def test_rate_limiter_blocks_after_limit() -> None:
    limiter = InMemoryRateLimiter()
    limiter.allow("key-b", 1)
    assert limiter.allow("key-b", 1) is False
