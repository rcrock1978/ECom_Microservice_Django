class ServiceRegistry:
    def services(self) -> list[str]:
        return [
            "auth-service",
            "product-service",
            "cart-service",
            "order-service",
            "coupon-service",
            "reward-service",
            "email-service",
        ]
