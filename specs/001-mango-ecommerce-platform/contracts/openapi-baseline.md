# OpenAPI Baseline Validation

This baseline confirms all gateway-exposed services have schema-ready settings and contract references before story implementation.

## Services covered

- Auth (`services/auth_service/auth_service/settings.py`)
- Product (`services/product_service/product_service/settings.py`)
- Cart (`services/cart_service/cart_service/settings.py`)
- Coupon (`services/coupon_service/coupon_service/settings.py`)
- Order (`services/order_service/order_service/settings.py`)
- Reward (`services/reward_service/reward_service/settings.py`)
- Email (`services/email_service/email_service/settings.py`)
- Gateway (`services/gateway/gateway/settings.py`)

## Contract references

- `auth-api.md`
- `product-api.md`
- `cart-api.md`
- `coupon-api.md`
- `order-api.md`
- `reward-api.md`
- `email-api.md`
- `gateway-routes.md`
- `message-bus-events.md`
