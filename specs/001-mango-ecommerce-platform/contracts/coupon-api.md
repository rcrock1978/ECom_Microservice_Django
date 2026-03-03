# API Contracts: Coupon Service

**Base URL**: `/api/v1/coupons/`  
**Upstream**: `http://coupon-service:8000`

---

## POST /api/v1/coupons/validate

Validate a coupon code for a given subtotal. Used by Cart and Order services.

**Auth Required**: Yes

**Request**:
```json
{
  "coupon_code": "SAVE20",
  "subtotal": "159.98"
}
```

**Response 200**:
```json
{
  "data": {
    "code": "SAVE20",
    "discount_type": "PERCENTAGE",
    "discount_value": "20.00",
    "calculated_discount": "32.00",
    "is_valid": true
  }
}
```

**Response 400** (invalid coupon):
```json
{
  "error": {
    "code": "COUPON_EXPIRED",
    "message": "This coupon has expired"
  }
}
```

Error codes: `COUPON_NOT_FOUND`, `COUPON_EXPIRED`, `COUPON_USAGE_LIMIT_REACHED`, `COUPON_MINIMUM_NOT_MET`, `COUPON_INACTIVE`

---

## POST /api/v1/coupons/redeem

Record coupon usage. Called by Order service after successful payment.

**Auth Required**: Yes (internal service call)

**Request**:
```json
{
  "coupon_code": "SAVE20",
  "order_id": "uuid",
  "user_id": "uuid",
  "discount_applied": "32.00"
}
```

**Response 200**: Usage recorded, `current_usage_count` incremented  
**Response 409**: Coupon already redeemed for this order (idempotent check)

---

## Admin: GET /api/v1/coupons/

List all coupons (admin only).

**Auth Required**: Yes (Admin role)

**Response 200**:
```json
{
  "data": [
    {
      "id": "uuid",
      "code": "SAVE20",
      "discount_type": "PERCENTAGE",
      "discount_value": "20.00",
      "minimum_purchase": "0.00",
      "max_usage_count": 100,
      "current_usage_count": 23,
      "expires_at": "2026-12-31T23:59:59Z",
      "is_active": true
    }
  ]
}
```

---

## Admin: POST /api/v1/coupons/

Create a new coupon (admin only).

**Auth Required**: Yes (Admin role)

**Request**:
```json
{
  "code": "SUMMER50",
  "discount_type": "FLAT_AMOUNT",
  "discount_value": "50.00",
  "minimum_purchase": "100.00",
  "max_usage_count": 200,
  "expires_at": "2026-09-01T00:00:00Z"
}
```

**Response 201**: Created coupon  
**Response 400**: Validation error (duplicate code, invalid values)

---

## Admin: PUT /api/v1/coupons/{id}/

Update a coupon (admin only).

**Auth Required**: Yes (Admin role)

**Response 200**: Updated coupon  
**Response 404**: Coupon not found

---

## Admin: DELETE /api/v1/coupons/{id}/

Deactivate a coupon (admin only). Sets `is_active` to false.

**Auth Required**: Yes (Admin role)

**Response 204**: Coupon deactivated
