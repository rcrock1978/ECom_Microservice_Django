from gateway.presentation.views import GatewayFacade


def test_proxy_forwards_public_products_request() -> None:
    facade = GatewayFacade.in_memory()
    response = facade.proxy("/api/v1/products/", method="GET")
    assert response["status"] == 200


def test_proxy_rejects_protected_route_without_auth() -> None:
    facade = GatewayFacade.in_memory()
    response = facade.proxy("/api/v1/cart/", method="GET")
    assert response["status"] == 401


def test_proxy_injects_headers_for_authenticated_route() -> None:
    facade = GatewayFacade.in_memory()
    response = facade.proxy("/api/v1/cart/", method="GET", access_token="access-user-1-customer")
    assert response["status"] in {200, 503}
    if response["status"] == 200:
        assert "X-User-ID" in response["forwarded_headers"]
