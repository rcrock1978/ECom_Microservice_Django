# API Contracts: Order Service

**Base URL**: `/api/v1/orders/`  
**Upstream**: `http://order-service:8000`

All order endpoints require authentication.

---

## POST /api/v1/orders/

Create an order from the current cart contents.

**Auth Required**: Yes

**Request**:
```json
{
  "shipping_name": "John Doe",
  "shipping_address": "123 Main St",
  "shipping_city": "New York",
  "shipping_state": "NY",
  "shipping_zip": "10001",
  "shipping_country": "US",
  "coupon_code": "SAVE20",
  "redeem_reward_points": 100
}
```

**Processing Flow**:
1. Fetch cart items for user (sync call to Cart service)
2. Validate product availability and prices (sync call to Product service)
3. Validate coupon if provided (sync call to Coupon service)
4. Validate reward points if provided (sync call to Reward service)
5. Calculate totals (subtotal - coupon_discount - reward_discount)
6. Create order with PENDING status
7. Initiate payment session with payment provider
8. Return order with payment redirect URL

**Response 201**:
```json
{
  "data": {
    "id": "uuid",
    "order_number": "ORD-20260304-001",
    "items": [
      {
        "product_id": "uuid",
        "product_name": "Wireless Headphones",
        "unit_price": "79.99",
        "quantity": 2,
        "line_total": "159.98"
      }
    ],
    "subtotal": "159.98",
    "coupon_code": "SAVE20",
    "coupon_discount": "32.00",
    "reward_points_used": 100,
    "reward_discount": "10.00",
    "total": "117.98",
    "status": "PENDING",
    "payment_url": "https://checkout.stripe.com/pay/cs_xxx",
    "shipping": {
      "name": "John Doe",
      "address": "123 Main St",
      "city": "New York",
      "state": "NY",
      "zip": "10001",
      "country": "US"
    },
    "created_at": "2026-03-04T14:30:00Z"
  }
}
```

**Response 400**: Empty cart, invalid shipping, coupon invalid, insufficient reward points  
**Response 409**: Product out of stock (with details of which items)

---

## GET /api/v1/orders/

List current user's orders (paginated, newest first).

**Auth Required**: Yes

**Query Parameters**:
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | int | 1 | Page number |
| `page_size` | int | 10 | Items per page (max 50) |
| `status` | string | — | Filter by status |

**Response 200**:
```json
{
  "data": [
    {
      "id": "uuid",
      "order_number": "ORD-20260304-001",
      "total": "117.98",
      "status": "CONFIRMED",
      "item_count": 2,
      "created_at": "2026-03-04T14:30:00Z"
    }
  ],
  "meta": {"page": 1, "page_size": 10, "total": 5}
}
```

---

## GET /api/v1/orders/{order_number}/

Get detailed order information.

**Auth Required**: Yes (order must belong to requesting user, or admin)

**Response 200**: Full order object (same format as POST response, minus payment_url)  
**Response 404**: Order not found or not owned by user

---

## POST /api/v1/orders/{order_number}/cancel

Cancel a pending or confirmed order (within cancellation policy).

**Auth Required**: Yes

**Response 200**: Updated order with status "CANCELLED"  
**Response 400**: Order cannot be cancelled (already shipped/delivered)  
**Side Effect**: Publishes `order.status_changed` event; inventory restored

---

## Webhook: POST /api/v1/orders/webhook/payment/

Payment provider webhook for async payment confirmations.

**Auth Required**: No (verified via webhook signature)

**Processing**:
- On payment success: Update order to CONFIRMED, publish `order.confirmed` event, clear cart
- On payment failure: Update order to CANCELLED, publish `payment.failed` event

---

## Admin: PUT /api/v1/orders/{order_number}/status/ (Admin)

Update order status (admin only — for shipping/delivery).

**Auth Required**: Yes (Admin role)

**Request**:
```json
{
  "status": "SHIPPED",
  "tracking_number": "1Z999AA10123456784"
}
```

**Response 200**: Updated order  
**Response 400**: Invalid status transition  
**Side Effect**: Publishes `order.status_changed` event
