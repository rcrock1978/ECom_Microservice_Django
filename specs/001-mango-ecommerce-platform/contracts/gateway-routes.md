# API Contracts: Gateway Routes

**Purpose**: Defines the unified API surface exposed by the gateway to the Next.js frontend.  
All endpoints use JSON request/response bodies. Authentication via httpOnly JWT cookie.

## Common Response Format

All services return errors in this format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [{"field": "email", "message": "Invalid email format"}]
  }
}
```

Success responses wrap data:
```json
{
  "data": { ... },
  "meta": {"page": 1, "page_size": 20, "total": 150}
}
```

## Gateway Route Map

| Route Prefix | Upstream Service | Auth Required | Rate Limit |
|-------------|-----------------|---------------|------------|
| `/api/v1/auth/` | auth-service:8000 | No (except /me, /logout) | 20 req/min (login/register) |
| `/api/v1/products/` | product-service:8000 | No (read), Yes (write) | 100 req/min |
| `/api/v1/categories/` | product-service:8000 | No (read), Yes (write) | 100 req/min |
| `/api/v1/cart/` | cart-service:8000 | Yes | 60 req/min |
| `/api/v1/orders/` | order-service:8000 | Yes | 30 req/min |
| `/api/v1/coupons/` | coupon-service:8000 | Yes | 30 req/min |
| `/api/v1/rewards/` | reward-service:8000 | Yes | 60 req/min |
| `/api/v1/admin/` | respective services | Yes (Admin role) | 100 req/min |

## Headers Injected by Gateway

| Header | Value | When |
|--------|-------|------|
| `X-Request-ID` | UUID v4 | Always (correlation ID) |
| `X-User-ID` | UUID from JWT | Authenticated requests |
| `X-User-Role` | "customer" or "admin" | Authenticated requests |
| `X-User-Email` | Email from JWT | Authenticated requests |
