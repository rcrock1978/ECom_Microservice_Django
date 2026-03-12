RATE_LIMITS: dict[str, int] = {
    "/api/v1/auth/": 20,
    "/api/v1/products/": 100,
    "/api/v1/categories/": 100,
    "/api/v1/cart/": 60,
    "/api/v1/orders/": 30,
    "/api/v1/coupons/": 30,
    "/api/v1/rewards/": 60,
}


def limit_for_path(path: str) -> int:
    for prefix, limit in RATE_LIMITS.items():
        if path.startswith(prefix):
            return limit
    return 30
