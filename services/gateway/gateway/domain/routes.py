SERVICE_ROUTES: dict[str, dict[str, object]] = {
    "/api/v1/auth/": {"upstream": "http://auth-service:8000", "auth_required": False, "service": "auth"},
    "/api/v1/products/": {"upstream": "http://product-service:8000", "auth_required": False, "service": "product"},
    "/api/v1/categories/": {"upstream": "http://product-service:8000", "auth_required": False, "service": "product"},
    "/api/v1/cart/": {"upstream": "http://cart-service:8000", "auth_required": True, "service": "cart"},
    "/api/v1/orders/": {"upstream": "http://order-service:8000", "auth_required": True, "service": "order"},
    "/api/v1/coupons/": {"upstream": "http://coupon-service:8000", "auth_required": True, "service": "coupon"},
    "/api/v1/rewards/": {"upstream": "http://reward-service:8000", "auth_required": True, "service": "reward"},
}


def match_route(path: str) -> dict[str, object] | None:
    for prefix, config in SERVICE_ROUTES.items():
        if path.startswith(prefix):
            return config
    return None
