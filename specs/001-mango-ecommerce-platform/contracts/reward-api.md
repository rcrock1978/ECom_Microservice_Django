# API Contracts: Reward Service

**Base URL**: `/api/v1/rewards/`  
**Upstream**: `http://reward-service:8000`

---

## GET /api/v1/rewards/

Get current user's reward account summary.

**Auth Required**: Yes

**Response 200**:
```json
{
  "data": {
    "current_balance": 350,
    "lifetime_earned": 1200,
    "points_expiring_soon": {
      "points": 50,
      "expires_at": "2026-04-15T00:00:00Z"
    },
    "minimum_redemption": 50,
    "points_to_dollar_rate": 0.10
  }
}
```

**Note**: Account is auto-created on first access (`user.registered` event or first GET).

---

## GET /api/v1/rewards/transactions/

Get reward points transaction history.

**Auth Required**: Yes

**Query Parameters**:
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | int | 1 | Page number |
| `page_size` | int | 20 | Items per page |
| `type` | string | — | Filter: `earned`, `redeemed`, `expired` |

**Response 200**:
```json
{
  "data": [
    {
      "id": "uuid",
      "transaction_type": "EARNED",
      "points": 50,
      "description": "Order ORD-20260304-001",
      "order_id": "uuid",
      "expires_at": "2027-03-04T00:00:00Z",
      "created_at": "2026-03-04T14:30:00Z"
    },
    {
      "id": "uuid",
      "transaction_type": "REDEEMED",
      "points": 100,
      "description": "Redeemed for order ORD-20260310-003",
      "order_id": "uuid",
      "expires_at": null,
      "created_at": "2026-03-10T09:00:00Z"
    }
  ],
  "meta": {"page": 1, "page_size": 20, "total": 12}
}
```

---

## POST /api/v1/rewards/validate-redemption

Check if user has enough points to redeem. Used by Order service during checkout.

**Auth Required**: Yes

**Request**:
```json
{
  "points": 100
}
```

**Response 200**:
```json
{
  "data": {
    "is_valid": true,
    "points_requested": 100,
    "dollar_value": "10.00",
    "current_balance": 350,
    "remaining_after_redemption": 250
  }
}
```

**Response 400**: Insufficient points or below minimum (50 points)

---

## POST /api/v1/rewards/redeem

Debit reward points. Called by Order service after successful payment.

**Auth Required**: Yes (internal service call)

**Request**:
```json
{
  "points": 100,
  "order_id": "uuid",
  "user_id": "uuid"
}
```

**Response 200**: Points debited  
**Response 409**: Already redeemed for this order (idempotent)  
**Response 400**: Insufficient balance

---

## Event Consumer: `order.confirmed`

When an `order.confirmed` event is received:
1. Calculate points earned (1 point per $1 of `total`)
2. Credit points to user's reward account
3. Set expiry to 12 months from now
4. Publish `reward.points_earned` event (consumed by Email service)

**Idempotency**: Unique constraint on (`account_id`, `order_id`, `EARNED`) prevents duplicate credits.
