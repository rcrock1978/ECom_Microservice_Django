from gateway.domain.routes import SERVICE_ROUTES, match_route


def test_match_route_returns_config_for_known_prefix() -> None:
    route = match_route("/api/v1/products/")
    assert route is not None
    assert route["upstream"].startswith("http://product-service")


def test_route_map_contains_auth_and_cart_prefixes() -> None:
    assert "/api/v1/auth/" in SERVICE_ROUTES
    assert "/api/v1/cart/" in SERVICE_ROUTES
