# API Contracts: Shopping Cart Service

**Base URL**: `/api/v1/cart/`  
**Upstream**: `http://cart-service:8000`

All cart endpoints require authentication.

---

## GET /api/v1/cart/

Get the current user's cart with all items. Creates an empty cart if none exists.

**Auth Required**: Yes

**Response 200**:
```json
{
  "data": {
    "id": "uuid",
    "items": [
      {
        "id": "uuid",
        "product_id": "uuid",
        "product_name": "Wireless Headphones",
        "product_price": "79.99",
        "quantity": 2,
        "line_total": "159.98"
      }
    ],
    "coupon_code": "SAVE20",
    "item_count": 2,
    "subtotal": "159.98"
  }
}
```

**Note**: On GET, the service refreshes product prices from the Product service to detect stale snapshots. If a product is no longer active, the item is flagged.

---

## POST /api/v1/cart/items/

Add an item to the cart. If the product already exists in the cart, increment quantity.

**Auth Required**: Yes

**Request**:
```json
{
  "product_id": "uuid",
  "quantity": 1
}
```

**Response 201**: Updated cart (same format as GET)  
**Response 400**: Invalid quantity or product unavailable  
**Response 409**: Product out of stock

---

## PUT /api/v1/cart/items/{item_id}/

Update the quantity of a cart item.

**Auth Required**: Yes

**Request**:
```json
{
  "quantity": 3
}
```

**Response 200**: Updated cart  
**Response 400**: Quantity < 1  
**Response 404**: Cart item not found

---

## DELETE /api/v1/cart/items/{item_id}/

Remove an item from the cart.

**Auth Required**: Yes

**Response 200**: Updated cart (remaining items)  
**Response 404**: Cart item not found

---

## POST /api/v1/cart/coupon/

Apply a coupon code to the cart.

**Auth Required**: Yes

**Request**:
```json
{
  "coupon_code": "SAVE20"
}
```

**Behavior**: Cart service calls Coupon service to validate. If valid, stores the code.  
**Response 200**: Updated cart with coupon applied  
**Response 400**: Invalid, expired, or ineligible coupon (with specific error message)

---

## DELETE /api/v1/cart/coupon/

Remove the applied coupon from the cart.

**Auth Required**: Yes

**Response 200**: Updated cart without coupon

---

## DELETE /api/v1/cart/

Clear the entire cart (used after order placement).

**Auth Required**: Yes

**Response 204**: Cart emptied
