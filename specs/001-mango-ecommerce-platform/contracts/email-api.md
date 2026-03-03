# API Contracts: Email Service

**Base URL**: `/api/v1/emails/` (admin only, for monitoring)  
**Upstream**: `http://email-service:8000`

The Email service is primarily event-driven — it consumes domain events from the message bus and sends transactional emails. It has minimal HTTP endpoints (admin monitoring only).

---

## Event Consumers

### Event: `user.registered`

**Payload**:
```json
{
  "event_id": "uuid",
  "event_type": "user.registered",
  "user_id": "uuid",
  "email": "john@example.com",
  "name": "John Doe",
  "timestamp": "2026-03-04T12:00:00Z"
}
```

**Action**: Send welcome/registration confirmation email  
**Template**: `REGISTRATION`

---

### Event: `user.password_reset_requested`

**Payload**:
```json
{
  "event_id": "uuid",
  "event_type": "user.password_reset_requested",
  "user_id": "uuid",
  "email": "john@example.com",
  "reset_link": "https://mango.example.com/reset-password?token=xxx",
  "expires_in_minutes": 30,
  "timestamp": "2026-03-04T12:00:00Z"
}
```

**Action**: Send password reset email with link  
**Template**: `PASSWORD_RESET`

---

### Event: `order.confirmed`

**Payload**:
```json
{
  "event_id": "uuid",
  "event_type": "order.confirmed",
  "order_id": "uuid",
  "order_number": "ORD-20260304-001",
  "user_id": "uuid",
  "email": "john@example.com",
  "items": [
    {"product_name": "Wireless Headphones", "quantity": 2, "unit_price": "79.99", "line_total": "159.98"}
  ],
  "subtotal": "159.98",
  "coupon_discount": "32.00",
  "reward_discount": "10.00",
  "total": "117.98",
  "shipping": {"name": "John Doe", "address": "123 Main St, New York, NY 10001"},
  "timestamp": "2026-03-04T14:30:00Z"
}
```

**Action**: Send order confirmation email with full order details  
**Template**: `ORDER_CONFIRMATION`

---

### Event: `order.status_changed`

**Payload**:
```json
{
  "event_id": "uuid",
  "event_type": "order.status_changed",
  "order_id": "uuid",
  "order_number": "ORD-20260304-001",
  "user_id": "uuid",
  "email": "john@example.com",
  "old_status": "CONFIRMED",
  "new_status": "SHIPPED",
  "tracking_number": "1Z999AA10123456784",
  "timestamp": "2026-03-05T16:00:00Z"
}
```

**Action**: Send order status update email  
**Template**: `ORDER_STATUS_UPDATE`

---

### Event: `payment.failed`

**Payload**:
```json
{
  "event_id": "uuid",
  "event_type": "payment.failed",
  "order_id": "uuid",
  "order_number": "ORD-20260304-001",
  "user_id": "uuid",
  "email": "john@example.com",
  "reason": "Card declined",
  "timestamp": "2026-03-04T14:35:00Z"
}
```

**Action**: Send payment failure notification  
**Template**: `PAYMENT_FAILED`

---

### Event: `reward.points_earned`

**Payload**:
```json
{
  "event_id": "uuid",
  "event_type": "reward.points_earned",
  "user_id": "uuid",
  "email": "john@example.com",
  "points_earned": 118,
  "new_balance": 468,
  "order_number": "ORD-20260304-001",
  "timestamp": "2026-03-04T14:31:00Z"
}
```

**Action**: Send reward points earned notification  
**Template**: `REWARD_MILESTONE`

---

## Email Delivery

- **Provider**: SMTP (configurable; SendGrid/Mailgun/AWS SES for production)
- **Retry Policy**: Max 3 retries with exponential backoff (30s, 120s, 480s)
- **Dead-Letter**: After 3 failed attempts, message status → `DEAD_LETTER`
- **Idempotency**: `event_id` ensures duplicate events don't produce duplicate emails

---

## Admin: GET /api/v1/emails/ (Admin)

List email messages for monitoring.

**Auth Required**: Yes (Admin role)

**Query Parameters**: `page`, `page_size`, `status` (PENDING/SENT/FAILED/DEAD_LETTER), `template_type`

**Response 200**:
```json
{
  "data": [
    {
      "id": "uuid",
      "recipient_email": "john@example.com",
      "template_type": "ORDER_CONFIRMATION",
      "subject": "Order Confirmed: ORD-20260304-001",
      "status": "SENT",
      "retry_count": 0,
      "created_at": "2026-03-04T14:30:05Z",
      "sent_at": "2026-03-04T14:30:08Z"
    }
  ]
}
```

## Admin: POST /api/v1/emails/{id}/retry (Admin)

Manually retry a failed/dead-letter email.

**Auth Required**: Yes (Admin role)

**Response 200**: Email re-queued  
**Response 404**: Email not found
