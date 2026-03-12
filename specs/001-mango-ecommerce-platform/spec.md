# Feature Specification: Mango Microservices E-Commerce Platform

**Feature Branch**: `001-mango-ecommerce-platform`  
**Created**: 2026-03-04  
**Status**: Draft  
**Input**: User description: "Mango Microservices is a full-stack e-commerce platform built with Python Django Framework architecture, enabling scalable online shopping with modular services. Includes Auth, Product, ShoppingCart, Order, Email, Coupon, Reward microservices with API Gateway, message bus, and NextJS frontend."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration and Authentication (Priority: P1)

A new customer visits the Mango storefront and creates an account by providing their name, email, and password. After registration, they receive a confirmation email and can log in. Returning users log in with their credentials and receive a secure session. Administrators can log in with elevated privileges to manage products, coupons, and orders.

**Why this priority**: Authentication is foundational — no other service (cart, orders, rewards) works without knowing who the user is. This is the critical path gatekeeper for the entire platform.

**Independent Test**: Can be fully tested by registering a new user, logging in, and verifying that a valid session token is issued. Delivers immediate value as the identity backbone for all services.

**Acceptance Scenarios**:

1. **Given** a visitor on the registration page, **When** they submit valid name, email, and password, **Then** an account is created, a confirmation email is sent, and they are redirected to the login page.
2. **Given** a registered user on the login page, **When** they enter valid credentials, **Then** they receive a JWT cookie and are redirected to the storefront homepage.
3. **Given** a registered user on the login page, **When** they enter an incorrect password 5 times, **Then** the account is temporarily locked for 15 minutes and the user is notified.
4. **Given** a logged-in user, **When** they request a password reset, **Then** they receive a password reset email with a secure, time-limited link.
5. **Given** an administrator, **When** they log in with admin credentials, **Then** they receive an elevated session with access to management features.

---

### User Story 2 - Browse and Search Product Catalog (Priority: P1)

A shopper browses the storefront and views a categorized list of products. They can filter by category, search by name or keyword, and view detailed product pages showing name, description, price, images, and availability status.

**Why this priority**: Product browsing is the primary customer entry point — users must see products before they can buy anything. Co-equal with auth as a platform foundation.

**Independent Test**: Can be tested by loading the storefront, verifying product listings display correctly, filtering by category, searching by keyword, and viewing a product detail page.

**Acceptance Scenarios**:

1. **Given** a visitor on the storefront homepage, **When** they browse the catalog, **Then** they see a paginated list of products with name, image, price, and category.
2. **Given** a visitor on the catalog page, **When** they select a category filter, **Then** only products in that category are displayed.
3. **Given** a visitor, **When** they search for "laptop", **Then** all products matching "laptop" in name or description are returned, sorted by relevance.
4. **Given** a visitor viewing a product detail page, **When** the product is out of stock, **Then** the page shows "Out of Stock" and disables the "Add to Cart" button.

---

### User Story 3 - Shopping Cart Management (Priority: P2)

A logged-in customer adds products to their shopping cart while browsing. They can view the cart, change item quantities, remove items, and see a running subtotal. The cart persists across sessions so items are not lost if the user logs out and returns later.

**Why this priority**: The cart bridges browsing and checkout. Without a cart, users cannot accumulate items for purchase. Depends on Auth (P1) and Products (P1).

**Independent Test**: Can be tested by logging in, adding multiple products to the cart, updating quantities, removing an item, logging out, logging back in, and verifying the cart state is preserved.

**Acceptance Scenarios**:

1. **Given** a logged-in user viewing a product, **When** they click "Add to Cart", **Then** the item appears in their cart with quantity 1 and the cart icon updates.
2. **Given** a user with items in the cart, **When** they increase the quantity of an item to 3, **Then** the subtotal recalculates accordingly.
3. **Given** a user with items in the cart, **When** they remove an item, **Then** the item is removed and the subtotal recalculates.
4. **Given** a user who logs out with items in the cart, **When** they log back in, **Then** their cart contents are preserved exactly as they left them.

---

### User Story 4 - Apply Coupons and Discounts (Priority: P2)

A customer at checkout enters a coupon code to receive a discount. The system validates the code, checks expiration and usage limits, and applies the discount (percentage or flat amount) to the order subtotal. Invalid or expired codes produce a clear error message.

**Why this priority**: Coupons drive conversions and promotions. Placed at P2 because it enhances the checkout flow but the platform can function without it.

**Independent Test**: Can be tested by creating a coupon (admin), adding items to cart, applying the coupon at checkout, and verifying the discount is reflected in the total.

**Acceptance Scenarios**:

1. **Given** a user at checkout with a $100 subtotal, **When** they apply a valid "20OFF" coupon (20% discount), **Then** the order total becomes $80.
2. **Given** a user at checkout, **When** they apply an expired coupon code, **Then** an error message "This coupon has expired" is displayed and no discount is applied.
3. **Given** a user at checkout, **When** they apply a coupon with a minimum purchase requirement of $50 but their subtotal is $30, **Then** an error message "Minimum purchase of $50 required" is displayed.
4. **Given** an admin, **When** they create a new coupon with a code, discount type, value, expiry date, and usage limit, **Then** the coupon is available for customers to use.

---

### User Story 5 - Place an Order and Process Payment (Priority: P2)

A customer with items in their cart proceeds to checkout, provides shipping details, reviews the order summary (including any applied coupons), and completes payment. Upon successful payment, the order is confirmed, inventory is updated, an order confirmation email is sent, and reward points are credited to the customer's account.

**Why this priority**: Order processing is the revenue-generating action. Placed at P2 because it depends on Auth, Products, and Cart being functional first.

**Independent Test**: Can be tested by completing a full purchase flow: add items to cart, proceed to checkout, enter shipping info, complete payment, and verify the order appears in order history with correct details.

**Acceptance Scenarios**:

1. **Given** a user at checkout with items in their cart, **When** they provide valid shipping details and complete payment, **Then** the order is created with status "Confirmed" and a confirmation email is sent.
2. **Given** a successful order, **When** the order is confirmed, **Then** product inventory quantities are decremented accordingly.
3. **Given** a user completing a purchase, **When** payment processing fails, **Then** the order is not created, the cart is preserved, and the user sees an error message with the option to retry.
4. **Given** a logged-in user, **When** they navigate to "My Orders", **Then** they see a chronological list of all past orders with status, date, items, and total.

---

### User Story 6 - Reward Points Program (Priority: P3)

A customer earns reward points on every purchase (e.g., 1 point per dollar spent). They can view their points balance and redeem points for discounts on future orders. Points have an expiration policy and a minimum redemption threshold.

**Why this priority**: Loyalty features drive repeat purchases but are not needed for core commerce functionality. Enhances retention after the platform is operational.

**Independent Test**: Can be tested by making a purchase, verifying points are credited, then starting a new order and redeeming points as a discount.

**Acceptance Scenarios**:

1. **Given** a customer who completes a $50 order, **When** the order is confirmed, **Then** 50 reward points are credited to their account.
2. **Given** a customer with 200 reward points, **When** they choose to redeem points at checkout, **Then** the equivalent discount is applied to the order total.
3. **Given** a customer with 10 reward points, **When** they try to redeem (minimum is 50), **Then** the system indicates insufficient points with a message showing the minimum required.
4. **Given** a customer viewing their account dashboard, **When** they check rewards, **Then** they see current balance, points history, and upcoming expirations.

---

### User Story 7 - Transactional Email Notifications (Priority: P3)

The system sends email notifications for key events: registration confirmation, password reset links, order confirmation with details, order status updates (shipped, delivered), and reward points milestones. Emails are sent asynchronously so they do not block the user experience.

**Why this priority**: Email is important for user trust and communication but the platform functions without it. Asynchronous delivery means it can be added without disrupting existing flows.

**Independent Test**: Can be tested by triggering each event (register, reset password, place order) and verifying the corresponding email is queued and delivered with correct content.

**Acceptance Scenarios**:

1. **Given** a new user registers, **When** registration succeeds, **Then** a welcome/confirmation email is sent to their address within 60 seconds.
2. **Given** a user places an order, **When** the order is confirmed, **Then** an order confirmation email with order number, items, and total is sent within 60 seconds.
3. **Given** the email service is temporarily unavailable, **When** an email send fails, **Then** the message is retried up to 3 times with exponential backoff, and the user's primary action is not blocked.

---

### User Story 8 - Admin Product Management (Priority: P3)

An administrator can create, update, and delete products in the catalog. They can manage categories, set prices, upload product images, and update inventory levels. Changes are reflected on the storefront in near-real-time.

**Why this priority**: Essential for ongoing operations but initial launch can work with pre-seeded catalog data. Admin features are needed for sustained operations, not for MVP launch.

**Independent Test**: Can be tested by logging in as admin, creating a new product with all fields, verifying it appears on the storefront, then updating its price and verifying the change is reflected.

**Acceptance Scenarios**:

1. **Given** an admin on the product management page, **When** they create a new product with name, description, price, category, image, and stock quantity, **Then** the product is saved and visible on the storefront.
2. **Given** an admin editing a product, **When** they update the price from $50 to $45, **Then** the storefront reflects the new price within 30 seconds.
3. **Given** an admin, **When** they delete a product that has no pending orders, **Then** the product is removed from the catalog.
4. **Given** an admin, **When** they attempt to delete a product associated with pending orders, **Then** the system prevents deletion and suggests deactivating instead.

---

### User Story 9 - API Gateway Routing and Cross-Cutting Concerns (Priority: P1)

All frontend requests are routed through a single API Gateway that directs traffic to the appropriate microservice. The gateway handles authentication token validation, rate limiting, request logging, and provides a unified API surface for the frontend.

**Why this priority**: The gateway is the single entry point for all frontend-to-backend communication. Without it, the frontend cannot reach any microservice. Infrastructure-critical.

**Independent Test**: Can be tested by sending requests to the gateway endpoint and verifying they are correctly routed to the target microservice, that unauthenticated requests to protected routes are rejected, and that rate limits are enforced.

**Acceptance Scenarios**:

1. **Given** a frontend request to `/api/v1/products/`, **When** the gateway receives it, **Then** the request is routed to the Product service and the response is returned to the frontend.
2. **Given** a request with a valid authentication token, **When** the gateway validates the token, **Then** the request is forwarded to the target service with user identity context.
3. **Given** a request without an authentication token to a protected endpoint, **When** the gateway receives it, **Then** a 401 Unauthorized response is returned.
4. **Given** a client exceeding the rate limit (e.g., 100 requests/minute), **When** they send another request, **Then** a 429 Too Many Requests response is returned.

---

### User Story 10 - Asynchronous Inter-Service Messaging (Priority: P2)

When key events occur (order placed, payment completed, inventory changed), the originating service publishes a message to the message bus. Subscribing services (Email, Reward, Inventory) consume these messages asynchronously. This ensures services are decoupled and failures in one service do not cascade to others.

**Why this priority**: Event-driven communication is the architectural backbone for decoupling services. Required before Order, Email, and Reward services can communicate reliably.

**Independent Test**: Can be tested by placing an order and verifying that the Email service receives the "order confirmed" event and sends a confirmation email, and the Reward service credits points — all without synchronous coupling.

**Acceptance Scenarios**:

1. **Given** a user places an order, **When** the Order service confirms it, **Then** an "OrderConfirmed" event is published to the message bus.
2. **Given** an "OrderConfirmed" event is published, **When** the Email service consumes it, **Then** an order confirmation email is sent to the customer.
3. **Given** an "OrderConfirmed" event is published, **When** the Reward service consumes it, **Then** reward points are credited to the customer's account.
4. **Given** the Email service is temporarily down, **When** an event is published, **Then** the message remains in the queue and is processed when the service recovers (no message loss).

---

### Edge Cases

- What happens when a user adds a product to the cart but it goes out of stock before checkout? The system validates inventory at checkout time and notifies the user of unavailable items.
- What happens when two users attempt to purchase the last item simultaneously? Inventory is decremented atomically; the second user receives an "out of stock" notification.
- What happens when the payment gateway times out? The order remains in "PENDING" status, the user is notified, and a background job retries or cancels after a configurable timeout (default 15 minutes).
- What happens when a coupon is applied but the cart total changes (items removed)? The coupon eligibility is re-validated whenever the cart changes; if the new total falls below the minimum, the coupon is removed with a notification.
- What happens when a microservice is unreachable? The API Gateway returns a 503 Service Unavailable with a user-friendly message, and the event bus ensures asynchronous messages are queued for retry.
- What happens when a user applies reward points and a coupon to the same order? Both discounts are applied — coupon discount first, then reward points on the remaining total. Combined discount cannot exceed 100% of the order total.
- What happens when an email fails to send after all retry attempts? The failed message is moved to a dead-letter queue for manual review; the user's transaction is not affected.

## Requirements *(mandatory)*

### Functional Requirements

**Authentication & Authorization**
- **FR-001**: System MUST allow users to register with name, email, and password.
- **FR-002**: System MUST authenticate users via email/password and issue JWT tokens for session management.
- **FR-003**: System MUST support role-based access control with at least "Customer" and "Admin" roles.
- **FR-004**: System MUST allow users to reset their password via a secure, time-limited email link.
- **FR-005**: System MUST temporarily lock accounts after 5 consecutive failed login attempts for 15 minutes.
- **FR-006**: System MUST support token refresh so users are not forced to re-authenticate during active sessions.

**Product Catalog**
- **FR-007**: System MUST display a paginated, searchable product catalog with name, image, price, category, and availability.
- **FR-008**: System MUST support product filtering by category.
- **FR-009**: System MUST support full-text search of product names and descriptions.
- **FR-010**: System MUST allow admins to create, read, update, and delete products.
- **FR-011**: System MUST allow admins to manage product categories.
- **FR-012**: System MUST track inventory quantities per product and display availability status.

**Shopping Cart**
- **FR-013**: System MUST allow logged-in users to add products to a shopping cart.
- **FR-014**: System MUST allow users to update item quantities and remove items from the cart.
- **FR-015**: System MUST persist cart contents across user sessions.
- **FR-016**: System MUST display a running subtotal that recalculates on every cart change.
- **FR-017**: System MUST validate product availability when items are added to the cart and at checkout.

**Coupons & Discounts**
- **FR-018**: System MUST allow admins to create coupons with code, discount type (percentage or flat), value, expiry date, minimum purchase amount, and usage limit.
- **FR-019**: System MUST validate coupon codes at checkout (existence, expiration, usage limits, minimum purchase).
- **FR-020**: System MUST apply valid coupon discounts to the order subtotal.
- **FR-021**: System MUST re-validate coupon eligibility when the cart changes.

**Orders & Payments**
- **FR-022**: System MUST allow users to place orders from their cart with shipping details.
- **FR-023**: System MUST integrate with a payment provider to process payments securely.
- **FR-024**: System MUST track order status through lifecycle stages (Pending, Confirmed, Shipped, Delivered, Cancelled).
- **FR-025**: System MUST provide order history to users with full order details.
- **FR-026**: System MUST decrement product inventory upon successful order confirmation.
- **FR-027**: System MUST handle payment failures gracefully without losing cart data.

**Rewards**
- **FR-028**: System MUST credit reward points to customers upon order confirmation (1 point per dollar spent).
- **FR-029**: System MUST allow customers to redeem reward points for discounts at checkout.
- **FR-030**: System MUST enforce a minimum points threshold for redemption (50 points).
- **FR-031**: System MUST display reward points balance, transaction history, and expiration on the user dashboard.
- **FR-032**: System MUST expire unused reward points after 12 months.

**Email Notifications**
- **FR-033**: System MUST send transactional emails for: registration confirmation, password reset, order confirmation, and order status updates.
- **FR-034**: System MUST send emails asynchronously without blocking user-facing operations.
- **FR-035**: System MUST retry failed email sends up to 3 times with exponential backoff.
- **FR-036**: System MUST route permanently failed emails to a dead-letter queue for manual review.

**API Gateway**
- **FR-037**: System MUST route all frontend requests through a single API Gateway to the appropriate microservice.
- **FR-038**: System MUST validate authentication tokens at the gateway level for protected endpoints.
- **FR-039**: System MUST enforce rate limiting per client (default: 100 requests/minute).
- **FR-040**: System MUST return appropriate HTTP error codes (401, 403, 429, 503) for gateway-level failures.

**Message Bus**
- **FR-041**: System MUST publish domain events (OrderConfirmed, InventoryUpdated, UserRegistered, etc.) to a message bus.
- **FR-042**: System MUST guarantee at-least-once delivery of messages.
- **FR-043**: Consuming services MUST process messages idempotently to handle potential duplicates.
- **FR-044**: System MUST support dead-letter queues for messages that fail processing after retries.

**General / Cross-Cutting**
- **FR-045**: Each microservice MUST be independently deployable as a containerized unit.
- **FR-046**: System MUST support horizontal scaling of individual services (each service is stateless and can run N replicas behind a load balancer with no shared in-memory state).
- **FR-047**: System MUST log all requests and significant events for observability.

### Key Entities

- **User**: Represents a customer or administrator. Key attributes: name, email, hashed password, role (Customer/Admin), account status, created date.
- **Product**: An item available for purchase. Key attributes: name, description, price, category, image URL, stock quantity, availability status.
- **Category**: A grouping for products. Key attributes: name, description, parent category (for hierarchy).
- **Cart**: A user's collection of items intended for purchase. Key attributes: owner (User), list of cart items, last updated timestamp.
- **CartItem**: A single product entry in a cart. Key attributes: product reference, quantity, unit price at time of addition.
- **Order**: A confirmed purchase transaction. Key attributes: customer (User), shipping details, list of order items, subtotal, discount, total, payment status, order status, timestamps.
- **OrderItem**: A single product entry in an order. Key attributes: product reference, quantity, unit price at time of purchase.
- **Coupon**: A discount code. Key attributes: code, discount type (percentage/flat), value, minimum purchase, expiry date, usage limit, current usage count.
- **RewardAccount**: A customer's loyalty points ledger. Key attributes: owner (User), current balance, lifetime earned.
- **RewardTransaction**: A single points credit or debit. Key attributes: account reference, points amount, transaction type (earned/redeemed/expired), related order, timestamp.
- **EmailMessage**: A queued email notification. Key attributes: recipient, subject, body/template, status (pending/sent/failed), retry count, event trigger.

## Assumptions

- The platform targets a standard B2C e-commerce audience (individual consumers purchasing products online).
- A single currency (USD) is used initially; multi-currency support is out of scope for this feature.
- Product images are uploaded and stored in external object storage; the Product service stores URLs/references only.
- Payment processing is delegated to a third-party payment provider; the platform does not store full credit card details.
- The reward points conversion rate is 1 point per $1 USD spent (configurable in the future).
- Email templates are pre-defined for each transactional email type; customizable email templates are out of scope.
- The platform launches in a single geographic region; multi-region deployment is a future enhancement.
- Product reviews/ratings are out of scope for this specification.
- Wishlist functionality is out of scope for this specification.
- Real-time inventory sync across warehouses is out of scope; inventory is managed as a single quantity per product.

## Success Criteria *(mandatory)*

Validation note: The performance and latency thresholds below are normative and must be used as pass/fail criteria in implementation validation (SC-002, SC-003, SC-009, SC-010).

### Measurable Outcomes

- **SC-001**: Users can complete the full purchase flow (register → browse → add to cart → checkout → receive confirmation) in under 5 minutes.
- **SC-002**: Platform supports at least 1,000 concurrent users browsing the catalog with <200ms p95 API response time.
- **SC-003**: 95% of product search queries return results in under 2 seconds.
- **SC-004**: Order confirmation emails are delivered within 60 seconds of order placement under normal conditions.
- **SC-005**: 90% of first-time users successfully complete their first purchase without requiring support assistance.
- **SC-006**: Individual microservices can be deployed independently without requiring downtime of other services.
- **SC-007**: A failure in one microservice (e.g., Email or Rewards) does not prevent users from browsing products, managing carts, or placing orders.
- **SC-008**: All domain events are delivered at least once to consuming services, with no permanent message loss.
- **SC-009**: Coupon validation and application completes within 1 second at checkout.
- **SC-010**: Reward points are credited to customer accounts within 30 seconds of order confirmation.
