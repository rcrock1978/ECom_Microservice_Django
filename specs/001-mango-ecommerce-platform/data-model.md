# Data Model: Mango Microservices E-Commerce Platform

**Created**: 2026-03-04  
**Feature**: 001-mango-ecommerce-platform  
**Spec**: [spec.md](spec.md) | **Research**: [research.md](research.md)

## Overview

Each microservice owns its database schema exclusively. Cross-service references use UUIDs as opaque identifiers — services never join across databases. Data consistency across services is achieved via domain events on the message bus.

All entities use UUIDs as primary keys for global uniqueness across services.

---

## Auth Service (`auth_schema`)

### User

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Unique user identifier |
| email | string(255) | UNIQUE, NOT NULL | Login email, validated format |
| name | string(150) | NOT NULL | Display name |
| password_hash | string(255) | NOT NULL | Argon2/bcrypt hashed password |
| role | enum | NOT NULL, default=CUSTOMER | CUSTOMER or ADMIN |
| is_active | boolean | NOT NULL, default=true | Account active status |
| is_email_verified | boolean | NOT NULL, default=false | Email verification status |
| failed_login_attempts | integer | NOT NULL, default=0 | Counter for lockout policy |
| locked_until | datetime | nullable | Account lockout expiry timestamp |
| created_at | datetime | NOT NULL | Registration timestamp |
| updated_at | datetime | NOT NULL | Last profile update |

**Indexes**: UNIQUE on `email`  
**Validation Rules**:
- Email must be valid format and unique
- Password minimum 8 characters, must contain uppercase, lowercase, and digit
- `failed_login_attempts` resets to 0 on successful login
- `locked_until` set to NOW + 15 minutes when `failed_login_attempts` reaches 5

### RefreshToken

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Token record identifier |
| user_id | UUID | FK → User, NOT NULL | Token owner |
| token_hash | string(255) | UNIQUE, NOT NULL | Hashed refresh token |
| expires_at | datetime | NOT NULL | Token expiry |
| is_blacklisted | boolean | NOT NULL, default=false | Revoked flag |
| created_at | datetime | NOT NULL | Issuance timestamp |

**Indexes**: UNIQUE on `token_hash`, INDEX on `user_id`  
**State Transitions**: Active → Blacklisted (on rotation or logout)

---

## Product Service (`product_schema`)

### Category

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Category identifier |
| name | string(100) | NOT NULL | Display name |
| slug | string(100) | UNIQUE, NOT NULL | URL-friendly identifier |
| description | text | nullable | Category description |
| parent_id | UUID | FK → Category, nullable | Parent for hierarchy |
| is_active | boolean | NOT NULL, default=true | Visibility flag |
| sort_order | integer | NOT NULL, default=0 | Display ordering |
| created_at | datetime | NOT NULL | Creation timestamp |
| updated_at | datetime | NOT NULL | Last update |

**Indexes**: UNIQUE on `slug`, INDEX on `parent_id`  
**Validation Rules**:
- Slug auto-generated from name if not provided
- Maximum hierarchy depth: 3 levels

### Product

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Product identifier |
| name | string(255) | NOT NULL | Product display name |
| slug | string(255) | UNIQUE, NOT NULL | URL-friendly identifier |
| description | text | NOT NULL | Full product description |
| price | decimal(10,2) | NOT NULL, CHECK > 0 | Current selling price in USD |
| category_id | UUID | FK → Category, NOT NULL | Product category |
| image_url | string(500) | nullable | Primary product image URL |
| stock_quantity | integer | NOT NULL, CHECK >= 0 | Available inventory count |
| is_active | boolean | NOT NULL, default=true | Visibility/purchasability flag |
| created_at | datetime | NOT NULL | Creation timestamp |
| updated_at | datetime | NOT NULL | Last update |

**Indexes**: UNIQUE on `slug`, INDEX on `category_id`, FULLTEXT on `name` + `description`  
**Validation Rules**:
- Price must be > 0
- Stock quantity must be >= 0
- Slug auto-generated from name if not provided
- `is_active` = false when soft-deleted (products with pending orders cannot be hard-deleted)

**State Transitions**:
- Active (is_active=true, stock > 0) → Out of Stock (is_active=true, stock = 0) → Active (restock)
- Active → Deactivated (is_active=false) → Active

---

## Shopping Cart Service (`cart_schema`)

### Cart

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Cart identifier |
| user_id | UUID | NOT NULL, UNIQUE | Cart owner (from Auth service, opaque UUID) |
| coupon_code | string(50) | nullable | Applied coupon code (validated at checkout) |
| created_at | datetime | NOT NULL | Cart creation timestamp |
| updated_at | datetime | NOT NULL | Last modification timestamp |

**Indexes**: UNIQUE on `user_id` (one active cart per user)

### CartItem

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Cart item identifier |
| cart_id | UUID | FK → Cart, NOT NULL | Parent cart |
| product_id | UUID | NOT NULL | Product reference (from Product service, opaque UUID) |
| product_name | string(255) | NOT NULL | Denormalized product name (snapshot) |
| product_price | decimal(10,2) | NOT NULL | Denormalized price at time of addition |
| quantity | integer | NOT NULL, CHECK > 0 | Item quantity |
| created_at | datetime | NOT NULL | Addition timestamp |
| updated_at | datetime | NOT NULL | Last quantity update |

**Indexes**: UNIQUE on (`cart_id`, `product_id`), INDEX on `cart_id`  
**Validation Rules**:
- Quantity must be >= 1; setting to 0 removes the item
- Product name and price are snapshots; can be refreshed from Product service on cart view
- Maximum 50 distinct items per cart

---

## Coupon Service (`coupon_schema`)

### Coupon

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Coupon identifier |
| code | string(50) | UNIQUE, NOT NULL | Redemption code (uppercase, alphanumeric) |
| discount_type | enum | NOT NULL | PERCENTAGE or FLAT_AMOUNT |
| discount_value | decimal(10,2) | NOT NULL, CHECK > 0 | Discount amount (% or USD) |
| minimum_purchase | decimal(10,2) | NOT NULL, default=0 | Minimum subtotal required |
| max_usage_count | integer | NOT NULL, default=0 | 0 = unlimited uses |
| current_usage_count | integer | NOT NULL, default=0 | Times redeemed |
| expires_at | datetime | NOT NULL | Coupon expiry timestamp |
| is_active | boolean | NOT NULL, default=true | Admin can disable |
| created_at | datetime | NOT NULL | Creation timestamp |
| updated_at | datetime | NOT NULL | Last update |

**Indexes**: UNIQUE on `code`  
**Validation Rules**:
- Code must be uppercase alphanumeric, 3-50 characters
- For PERCENTAGE type: discount_value must be between 0.01 and 100.00
- For FLAT_AMOUNT type: discount_value must be > 0
- `expires_at` must be in the future at creation time
- Coupon is valid when: `is_active` = true AND `expires_at` > NOW AND (`max_usage_count` = 0 OR `current_usage_count` < `max_usage_count`)

### CouponUsage

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Usage record identifier |
| coupon_id | UUID | FK → Coupon, NOT NULL | Coupon used |
| user_id | UUID | NOT NULL | User who redeemed (opaque UUID) |
| order_id | UUID | NOT NULL | Order where applied (opaque UUID) |
| discount_applied | decimal(10,2) | NOT NULL | Actual discount amount applied |
| used_at | datetime | NOT NULL | Redemption timestamp |

**Indexes**: INDEX on `coupon_id`, INDEX on `user_id`, UNIQUE on (`coupon_id`, `order_id`)

---

## Order Service (`order_schema`)

### Order

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Order identifier |
| user_id | UUID | NOT NULL | Customer (opaque UUID from Auth) |
| order_number | string(20) | UNIQUE, NOT NULL | Human-readable order number (e.g., ORD-20260304-001) |
| subtotal | decimal(10,2) | NOT NULL | Sum of item prices before discounts |
| coupon_code | string(50) | nullable | Applied coupon code |
| coupon_discount | decimal(10,2) | NOT NULL, default=0 | Discount from coupon |
| reward_points_used | integer | NOT NULL, default=0 | Points redeemed |
| reward_discount | decimal(10,2) | NOT NULL, default=0 | Discount from reward points |
| total | decimal(10,2) | NOT NULL | Final amount charged (subtotal - discounts) |
| status | enum | NOT NULL, default=PENDING | Order lifecycle status |
| payment_intent_id | string(255) | nullable | External payment provider reference |
| payment_status | enum | NOT NULL, default=PENDING | PENDING, COMPLETED, FAILED, REFUNDED |
| shipping_name | string(150) | NOT NULL | Recipient name |
| shipping_address | text | NOT NULL | Full shipping address |
| shipping_city | string(100) | NOT NULL | City |
| shipping_state | string(100) | NOT NULL | State/province |
| shipping_zip | string(20) | NOT NULL | Postal code |
| shipping_country | string(2) | NOT NULL, default=US | ISO country code |
| created_at | datetime | NOT NULL | Order placement timestamp |
| updated_at | datetime | NOT NULL | Last status change |

**Indexes**: UNIQUE on `order_number`, INDEX on `user_id`, INDEX on `status`, INDEX on `created_at`  
**Validation Rules**:
- `total` must be >= 0 (can be 0 if fully covered by coupons/rewards)
- `total` = `subtotal` - `coupon_discount` - `reward_discount`
- Combined discounts cannot exceed `subtotal`

**State Transitions**:
```
PENDING → CONFIRMED (payment successful)
PENDING → CANCELLED (payment failed or timeout after 15 min)
CONFIRMED → SHIPPED (admin updates)
SHIPPED → DELIVERED (admin updates or carrier webhook)
CONFIRMED → CANCELLED (admin or customer cancellation within policy)
```

### OrderItem

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Order item identifier |
| order_id | UUID | FK → Order, NOT NULL | Parent order |
| product_id | UUID | NOT NULL | Product reference (opaque UUID) |
| product_name | string(255) | NOT NULL | Product name at time of purchase |
| unit_price | decimal(10,2) | NOT NULL | Price per unit at time of purchase |
| quantity | integer | NOT NULL, CHECK > 0 | Quantity ordered |
| line_total | decimal(10,2) | NOT NULL | unit_price × quantity |
| created_at | datetime | NOT NULL | Row creation timestamp |

**Indexes**: INDEX on `order_id`, INDEX on `product_id`  
**Validation Rules**:
- `line_total` = `unit_price` × `quantity`
- Product name and price are immutable snapshots

---

## Reward Service (`reward_schema`)

### RewardAccount

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Account identifier |
| user_id | UUID | UNIQUE, NOT NULL | Account owner (opaque UUID) |
| current_balance | integer | NOT NULL, default=0, CHECK >= 0 | Available redeemable points |
| lifetime_earned | integer | NOT NULL, default=0 | Total points ever earned |
| created_at | datetime | NOT NULL | Account creation timestamp |
| updated_at | datetime | NOT NULL | Last balance change |

**Indexes**: UNIQUE on `user_id`

### RewardTransaction

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Transaction identifier |
| account_id | UUID | FK → RewardAccount, NOT NULL | Parent account |
| transaction_type | enum | NOT NULL | EARNED, REDEEMED, EXPIRED |
| points | integer | NOT NULL, CHECK > 0 | Points amount (always positive) |
| order_id | UUID | nullable | Related order (opaque UUID from Order service) |
| description | string(255) | NOT NULL | Human-readable description |
| expires_at | datetime | nullable | Point expiry (only for EARNED type, 12 months from creation) |
| created_at | datetime | NOT NULL | Transaction timestamp |

**Indexes**: INDEX on `account_id`, INDEX on `order_id`, INDEX on `expires_at`  
**Validation Rules**:
- EARNED: Increases `current_balance` and `lifetime_earned`
- REDEEMED: Decreases `current_balance`; minimum 50 points to redeem
- EXPIRED: Decreases `current_balance`; batch job runs nightly for points past `expires_at`
- Idempotency: UNIQUE constraint on (`account_id`, `order_id`, `transaction_type`) prevents duplicate credits from re-delivered events

**State Transitions (points lifecycle)**:
```
Points Earned (order confirmed) → Active → Redeemed (used at checkout)
                                        → Expired (12 months passed)
```

---

## Email Service (`email_schema`)

### EmailMessage

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK | Message identifier |
| recipient_email | string(255) | NOT NULL | Destination email address |
| recipient_name | string(150) | nullable | Recipient display name |
| template_type | enum | NOT NULL | REGISTRATION, PASSWORD_RESET, ORDER_CONFIRMATION, ORDER_STATUS_UPDATE, PAYMENT_FAILED, REWARD_MILESTONE |
| subject | string(255) | NOT NULL | Email subject line |
| template_data | jsonb | NOT NULL | Template variables (order details, reset link, etc.) |
| status | enum | NOT NULL, default=PENDING | Delivery status |
| retry_count | integer | NOT NULL, default=0 | Delivery attempt count |
| last_error | text | nullable | Last delivery error message |
| event_id | UUID | nullable | Source event ID for idempotency |
| created_at | datetime | NOT NULL | Queue timestamp |
| sent_at | datetime | nullable | Successful delivery timestamp |
| updated_at | datetime | NOT NULL | Last status change |

**Indexes**: INDEX on `status`, INDEX on `event_id` (UNIQUE when not null), INDEX on `created_at`  
**Validation Rules**:
- `retry_count` max = 3; after 3 failures, status transitions to DEAD_LETTER
- `event_id` ensures idempotency — duplicate events produce no additional emails

**State Transitions**:
```
PENDING → SENDING → SENT (success)
SENDING → FAILED (delivery error) → PENDING (retry, if retry_count < 3)
FAILED → DEAD_LETTER (retry_count >= 3)
```

---

## Cross-Service Reference Strategy

Services reference entities from other services using **opaque UUIDs**. They store the UUID as a plain field (not a foreign key) and may cache denormalized data for display purposes.

| Service | References | How |
|---------|-----------|-----|
| Cart | User (user_id) | Opaque UUID, set from gateway header |
| Cart | Product (product_id, product_name, product_price) | Opaque UUID + denormalized snapshot, refreshed on cart view via sync HTTP call to Product service |
| Order | User (user_id) | Opaque UUID |
| Order | Product (product_id, product_name, unit_price) | Immutable snapshot at order time |
| Coupon | User (user_id), Order (order_id) | Opaque UUIDs in CouponUsage |
| Reward | User (user_id), Order (order_id) | Opaque UUIDs |
| Email | User (recipient_email) | Email address copied from event payload |

**Data Consistency**: Eventual consistency via domain events. When a product price changes, existing cart snapshots are stale until the cart is viewed (lazy refresh). Order snapshots are immutable (price at time of purchase).

---

## Domain Events

Events published to the message bus that trigger cross-service data updates:

| Event | Publisher | Consumers | Payload |
|-------|----------|-----------|---------|
| `user.registered` | Auth | Email | user_id, email, name |
| `user.password_reset_requested` | Auth | Email | user_id, email, reset_token |
| `order.confirmed` | Order | Email, Reward, Product (inventory) | order_id, user_id, items[], total, email |
| `order.status_changed` | Order | Email | order_id, user_id, old_status, new_status, email |
| `inventory.low_stock` | Product | Email (admin notification) | product_id, product_name, stock_quantity |
| `reward.points_earned` | Reward | Email | user_id, email, points, new_balance |
| `payment.completed` | Order | (internal) | order_id, payment_intent_id, amount |
| `payment.failed` | Order | Email | order_id, user_id, email, reason |
