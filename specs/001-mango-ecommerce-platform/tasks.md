# Tasks: Mango Microservices E-Commerce Platform

**Input**: Design documents from `/specs/001-mango-ecommerce-platform/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: Included per Constitution Principle III (Test-First Development, NON-NEGOTIABLE). Test tasks appear BEFORE implementation in each user story phase. Tests MUST be written first and verified to FAIL before implementing the production code. Minimum 80% code coverage per service.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on in-progress tasks)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend services**: `services/{service_name}/`
- **Shared library**: `shared/`
- **Frontend**: `frontend/src/`
- Each backend service follows Clean Architecture layers: `domain/`, `application/`, `infrastructure/`, `presentation/`
- Domain layer has **ZERO Django imports** — plain Python dataclasses only

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the monorepo structure, initialize all projects, and configure the containerized development environment.

- [ ] T001 Create monorepo directory structure per plan.md project tree (services/, shared/, frontend/, specs/, docker/)
- [ ] T002 [P] Create root docker-compose.yml with PostgreSQL 16, RabbitMQ 3.13 (management), Redis 7, and pgAdmin in docker-compose.yml
- [ ] T003 [P] Create environment variable templates for all services in .env.example and services/*/.env.example
- [ ] T004 [P] Initialize shared library package with Poetry in shared/pyproject.toml (message_bus, common, testing subpackages)
- [ ] T005 Initialize all 8 Django service projects with Poetry, manage.py, settings, and WSGI/ASGI in services/*/pyproject.toml
- [ ] T006 [P] Initialize Next.js 14 frontend project with pnpm, TypeScript 5.x, and App Router in frontend/package.json
- [ ] T007 [P] Create multi-stage Dockerfile for Django services (shared base) in services/*/Dockerfile
- [ ] T008 [P] Create multi-stage Dockerfile for Next.js frontend in frontend/Dockerfile
- [ ] T009 Add all application services (8 Django + 1 Next.js + Celery workers) to docker-compose.yml
- [ ] T010 [P] Create root README.md with project overview, architecture summary, and quickstart reference

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement shared library, base configurations, and infrastructure code that ALL user stories depend on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T011 Implement event envelope and base event classes (BaseEvent, EventEnvelope with correlation_id, timestamp, routing_key) in shared/message_bus/events.py
- [ ] T012 [P] Implement Celery task publisher with publisher confirms and serialization in shared/message_bus/publisher.py
- [ ] T013 [P] Implement base consumer with idempotency check (ProcessedEvent) and exponential backoff retry in shared/message_bus/consumer.py
- [ ] T014 [P] Implement standard exception types (NotFoundError, ValidationError, ConflictError, UnauthorizedError, ForbiddenError) in shared/common/exceptions.py
- [ ] T015 [P] Implement consistent API response helpers (success_response, error_response, paginated_response) in shared/common/responses.py
- [ ] T016 [P] Implement correlation ID middleware and structured JSON logging configuration in shared/common/middleware.py
- [ ] T017 [P] Implement shared test utilities (base model factory, API test case mixin, event test helpers) in shared/testing/factories.py and shared/testing/fixtures.py
- [ ] T018 Configure base Django settings module for all services (DATABASE per schema, CACHES with Redis, CELERY_BROKER, INSTALLED_APPS, shared lib as editable dep) in services/*/config/settings.py
- [ ] T019 [P] Configure DRF defaults (PageNumberPagination, JWT authentication class, custom exception handler, JSON renderer) per service in services/*/config/settings.py
- [ ] T020 [P] Create ProcessedEvent Django model for idempotent message consumption in shared/common/models.py
- [ ] T021 [P] Create health check endpoint mixin (liveness + readiness with DB/Redis/RabbitMQ checks) in shared/common/health.py
- [ ] T022 [P] Configure Celery app with RabbitMQ broker, task serialization, and result backend per service in services/*/config/celery.py
- [ ] T023 [P] Create frontend TypeScript type definitions (User, Product, Category, Cart, Order, Coupon, Reward, ApiResponse, PaginatedResponse) in frontend/src/types/
- [ ] T024 [P] Create frontend API client (fetch wrapper with httpOnly cookie auth, error handling, base URL config) in frontend/src/lib/api/client.ts
- [ ] T025 [P] Create frontend auth context provider (login/logout/register, current user state, token refresh) in frontend/src/lib/auth/context.tsx
- [ ] T026 [P] Create frontend cart context provider (cart state, add/remove/update, item count badge) in frontend/src/lib/cart/context.tsx
- [ ] T027 [P] Create frontend layout components (Header with nav/auth/cart, Footer, MainLayout) in frontend/src/components/layout/
- [ ] T028 Create frontend root layout with providers, global styles, and metadata in frontend/src/app/layout.tsx

**Checkpoint**: Foundation ready — shared library, base configs, and frontend scaffolding complete. User story implementation can now begin.

---

## Phase 3: User Story 9 — API Gateway Routing and Cross-Cutting Concerns (Priority: P1) 🎯 MVP

**Goal**: All frontend requests route through a single API Gateway that validates JWT tokens, enforces rate limits, injects user context headers, and provides unified error responses.

**Independent Test**: Send requests to gateway endpoints and verify correct routing to target services, that unauthenticated requests to protected routes return 401, and that rate limits return 429.

### Tests for User Story 9 (Write FIRST — must FAIL before implementation)

- [ ] T139 [P] [US9] Unit tests for JWT token validation and rate limiting rules in services/gateway/tests/unit/test_jwt_validator.py and test_rate_limiter.py
- [ ] T140 [US9] Integration tests for proxy routing, auth rejection (401), and rate limit enforcement (429) in services/gateway/tests/integration/test_proxy.py

### Implementation for User Story 9

- [ ] T029 [US9] Create gateway domain layer: route configuration mapping (prefix → service URL, auth required flag) in services/gateway/gateway/domain/routes.py
- [ ] T030 [P] [US9] Create rate limit rule definitions (per-route limits: 20/min auth, 100/min products, 60/min cart, 30/min orders) in services/gateway/gateway/domain/rate_limits.py
- [ ] T031 [US9] Implement proxy use case (match route, check auth, check rate limit, forward request, return response) in services/gateway/gateway/application/proxy.py
- [ ] T032 [P] [US9] Implement service health aggregator use case (check all downstream services) in services/gateway/gateway/application/health.py
- [ ] T033 [US9] Implement httpx async proxy client with configurable timeouts and circuit breaker in services/gateway/gateway/infrastructure/proxy_client.py
- [ ] T034 [P] [US9] Implement JWT token validation (decode access_token cookie, verify signature/expiry, extract user_id/role/email) in services/gateway/gateway/infrastructure/jwt_validator.py
- [ ] T035 [P] [US9] Implement Redis-based sliding window rate limiter in services/gateway/gateway/infrastructure/rate_limiter.py
- [ ] T036 [US9] Create gateway middleware stack (correlation ID injection, auth validation, rate limiting, request/response logging) in services/gateway/gateway/presentation/middleware.py
- [ ] T037 [US9] Create gateway catch-all proxy view that handles all /api/v1/* requests in services/gateway/gateway/presentation/views.py
- [ ] T038 [US9] Configure gateway URL routing and Django settings in services/gateway/gateway/presentation/urls.py and services/gateway/config/urls.py

**Checkpoint**: Gateway proxies requests to backend services with JWT validation, rate limiting, and header injection (X-User-ID, X-User-Role, X-User-Email, X-Request-ID).

---

## Phase 4: User Story 1 — User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Users can register with name/email/password, log in to receive secure JWT session cookies, refresh tokens, reset passwords, and admins get elevated access.

**Independent Test**: Register a new user, log in, verify httpOnly JWT cookie is set, access GET /auth/me, log out, verify session is invalidated. Test account lockout after 5 failed attempts.

### Tests for User Story 1 (Write FIRST — must FAIL before implementation)

- [X] T141 [P] [US1] Unit tests for User entity, Email/Password value objects, and account lockout logic in services/auth_service/tests/unit/test_entities.py and test_use_cases.py
- [X] T142 [US1] Integration tests for register, login, refresh, logout, me, forgot-password, reset-password endpoints in services/auth_service/tests/integration/test_auth_api.py

### Implementation for User Story 1

- [X] T039 [P] [US1] Create auth domain layer (User entity dataclass, Email/Password/Role value objects, UserRepository ABC, UserRegistered/PasswordResetRequested events) in services/auth_service/auth/domain/
- [X] T040 [US1] Implement auth application use cases (RegisterUser, LoginUser, RefreshToken, LogoutUser, GetProfile, ForgotPassword, ResetPassword) with account lockout logic in services/auth_service/auth/application/
- [X] T041 [US1] Create auth Django ORM models (User with Argon2 password, RefreshToken with hash) and generate migrations in services/auth_service/auth/infrastructure/models.py
- [X] T042 [P] [US1] Implement DjangoUserRepository (CRUD, find_by_email, increment_failed_attempts, lock/unlock) in services/auth_service/auth/infrastructure/repositories.py
- [X] T043 [P] [US1] Implement JWT provider (issue access token 15min, refresh token 7d, httpOnly Secure SameSite=Lax cookies) in services/auth_service/auth/infrastructure/jwt_provider.py
- [X] T044 [US1] Implement event publisher for user.registered and user.password_reset_requested events in services/auth_service/auth/infrastructure/event_publisher.py
- [X] T045 [US1] Create DRF serializers (RegisterSerializer, LoginSerializer, TokenRefreshSerializer, ForgotPasswordSerializer, ResetPasswordSerializer, UserProfileSerializer) in services/auth_service/auth/presentation/serializers.py
- [X] T046 [US1] Create DRF views (RegisterView, LoginView, RefreshView, LogoutView, MeView, ForgotPasswordView, ResetPasswordView) in services/auth_service/auth/presentation/views.py
- [X] T047 [US1] Configure auth service URL routing (all /auth/* endpoints) in services/auth_service/auth/presentation/urls.py and services/auth_service/config/urls.py
- [ ] T048 [P] [US1] Create frontend login page (email/password form, validation, error display, redirect on success) in frontend/src/app/(auth)/login/page.tsx
- [ ] T049 [P] [US1] Create frontend register page (name/email/password form, validation, success message, redirect to login) in frontend/src/app/(auth)/register/page.tsx
- [ ] T050 [P] [US1] Create frontend forgot-password page and reset-password page (email form, token-based reset form) in frontend/src/app/(auth)/forgot-password/page.tsx and frontend/src/app/(auth)/reset-password/page.tsx
- [ ] T051 [US1] Wire frontend auth pages to API client, update auth context on login/logout, add protected route wrapper in frontend/src/lib/auth/

**Checkpoint**: Users can register, log in (JWT cookies set), access protected profile endpoint, and reset passwords. Frontend auth flow is complete through the gateway.

---

## Phase 5: User Story 2 — Browse and Search Product Catalog (Priority: P1) 🎯 MVP

**Goal**: Shoppers browse a categorized product catalog with pagination, search by keyword (full-text), filter by category/price/stock, and view detailed product pages.

**Independent Test**: Load storefront, verify product listings render with images/prices, search for a keyword, filter by category, navigate to product detail page and verify all fields display.

### Tests for User Story 2 (Write FIRST — must FAIL before implementation)

- [ ] T143 [P] [US2] Unit tests for Product/Category entities and search/filter domain logic in services/product_service/tests/unit/test_entities.py
- [ ] T144 [US2] Integration tests for product list/search/filter, category tree, and internal product lookup endpoints in services/product_service/tests/integration/test_product_api.py

### Implementation for User Story 2

- [ ] T052 [P] [US2] Create product domain layer (Product entity, Category entity, ProductRepository ABC, CategoryRepository ABC) in services/product_service/catalog/domain/
- [ ] T053 [US2] Implement product application use cases (ListProducts with filtering/sorting, SearchProducts full-text, GetProductBySlug, ListCategories tree) in services/product_service/catalog/application/
- [ ] T054 [US2] Create product Django ORM models (Product with full-text index, Category with self-referential parent) and generate migrations in services/product_service/catalog/infrastructure/models.py
- [ ] T055 [P] [US2] Implement DjangoProductRepository with full-text search (SearchVector/SearchRank), filtering, and pagination in services/product_service/catalog/infrastructure/repositories.py
- [ ] T056 [P] [US2] Implement DjangoCategoryRepository with nested tree traversal (max 3 levels) in services/product_service/catalog/infrastructure/repositories.py
- [ ] T057 [US2] Create DRF serializers (ProductListSerializer, ProductDetailSerializer, CategorySerializer, CategoryTreeSerializer) in services/product_service/catalog/presentation/serializers.py
- [ ] T058 [US2] Create DRF views (ProductListView with query filters, ProductDetailView by slug, CategoryListView, InternalProductView by UUID) in services/product_service/catalog/presentation/views.py
- [ ] T059 [US2] Configure product service URL routing (/products/*, /categories/*, /internal/products/*) in services/product_service/catalog/presentation/urls.py and services/product_service/config/urls.py
- [ ] T060 [P] [US2] Create frontend product catalog page (product grid, category sidebar, search bar, pagination controls) in frontend/src/app/products/page.tsx
- [ ] T061 [P] [US2] Create frontend product detail page (images, description, price, availability, Add to Cart button) in frontend/src/app/products/[slug]/page.tsx
- [ ] T062 [P] [US2] Create frontend product card and product grid reusable components in frontend/src/components/products/ProductCard.tsx and ProductGrid.tsx
- [ ] T063 [US2] Create seed data management command with sample products (10+) and categories (5+) in services/product_service/catalog/management/commands/seed_products.py

**Checkpoint**: Product catalog is browsable with search, category filtering, and detail pages working end-to-end through the gateway. Seed data available.

---

## Phase 6: User Story 10 — Asynchronous Inter-Service Messaging (Priority: P2)

**Goal**: Services communicate asynchronously via domain events on RabbitMQ with topic exchange routing. Events are published reliably with at-least-once delivery and consumed idempotently.

**Independent Test**: Publish a test event from one service and verify it is consumed by target service(s) without synchronous coupling. Verify dead-letter queues capture messages that fail after 3 retries.

### Tests for User Story 10 (Write FIRST — must FAIL before implementation)

- [ ] T145 [US10] Integration test for event publish-consume round trip, idempotency deduplication, and DLQ routing in shared/testing/test_message_bus.py

### Implementation for User Story 10

- [ ] T064 [US10] Define all 8 event types with routing keys and typed payload dataclasses (auth.user.registered, auth.user.password_reset_requested, order.order.confirmed, order.order.status_changed, order.payment.completed, order.payment.failed, product.inventory.low_stock, reward.points.earned) in shared/message_bus/events.py
- [ ] T065 [P] [US10] Configure RabbitMQ exchanges (mango.events topic durable, mango.dlx dead-letter fanout) and connection settings in shared/message_bus/config.py
- [ ] T066 [US10] Create queue binding declarations mapping routing keys to consumer queues per service (email.events, reward.events, product.events) in shared/message_bus/bindings.py
- [ ] T067 [P] [US10] Create Celery worker entry points and task registration per consuming service (product, reward, email) in services/*/config/celery.py
- [ ] T068 [P] [US10] Create ProcessedEvent migration for each consuming service (product_service, reward_service, email_service) in services/*/migrations/
- [ ] T069 [US10] Implement dead-letter queue consumer and admin monitoring helpers in shared/message_bus/dlq.py

**Checkpoint**: Message bus infrastructure is operational — publish, consume, retry, and DLQ flows are verified.

---

## Phase 7: User Story 3 — Shopping Cart Management (Priority: P2)

**Goal**: Logged-in users add products to a persistent cart, update quantities, remove items, apply/remove coupons, and see running subtotals. Cart persists across sessions.

**Independent Test**: Log in, add multiple products to cart, update quantity, remove an item, verify subtotal recalculates, log out, log back in, verify cart is preserved.

### Tests for User Story 3 (Write FIRST — must FAIL before implementation)

- [ ] T146 [P] [US3] Unit tests for Cart entity, item quantity validation, max 50 items limit, and subtotal calculation in services/cart_service/tests/unit/test_entities.py
- [ ] T147 [US3] Integration tests for cart CRUD, coupon application/removal, and product price refresh in services/cart_service/tests/integration/test_cart_api.py

### Implementation for User Story 3

- [ ] T070 [P] [US3] Create cart domain layer (Cart entity, CartItem entity, CartRepository ABC, validation rules: max 50 items, quantity >= 1) in services/cart_service/cart/domain/
- [ ] T071 [US3] Implement cart application use cases (GetOrCreateCart, AddItem, UpdateItemQuantity, RemoveItem, ClearCart, ApplyCoupon, RemoveCoupon; auto re-validate applied coupon on every cart change per FR-021) in services/cart_service/cart/application/
- [ ] T072 [US3] Create cart Django ORM models (Cart with unique user_id, CartItem with unique cart+product) and generate migrations in services/cart_service/cart/infrastructure/models.py
- [ ] T073 [P] [US3] Implement DjangoCartRepository in services/cart_service/cart/infrastructure/repositories.py
- [ ] T074 [US3] Implement product price refresh client (httpx GET to Product service /internal/products/{id}) in services/cart_service/cart/infrastructure/product_client.py
- [ ] T075 [P] [US3] Implement coupon validation client (httpx POST to Coupon service /coupons/validate) in services/cart_service/cart/infrastructure/coupon_client.py
- [ ] T076 [US3] Create DRF serializers (CartSerializer, CartItemSerializer, AddItemSerializer, UpdateQuantitySerializer, ApplyCouponSerializer) in services/cart_service/cart/presentation/serializers.py
- [ ] T077 [US3] Create DRF views (CartView GET/DELETE, CartItemView POST/PUT/DELETE, CartCouponView POST/DELETE) in services/cart_service/cart/presentation/views.py
- [ ] T078 [US3] Configure cart service URL routing (/cart/*, /cart/items/*, /cart/coupon/*) in services/cart_service/cart/presentation/urls.py and services/cart_service/config/urls.py
- [ ] T079 [P] [US3] Create frontend cart page (item list, quantity controls, remove button, subtotal, coupon input) and cart drawer component in frontend/src/app/cart/page.tsx and frontend/src/components/cart/
- [ ] T080 [US3] Integrate cart UI with cart context provider and wire Add to Cart button on product pages in frontend/src/lib/cart/

**Checkpoint**: Cart management works end-to-end through the gateway. Items persist across sessions, prices refresh from Product service, and coupon application previews discount.

---

## Phase 8: User Story 4 — Apply Coupons and Discounts (Priority: P2)

**Goal**: Customers apply coupon codes for percentage or flat-amount discounts with full validation (expiry, usage limits, minimum purchase). Admins CRUD coupons.

**Independent Test**: Create a coupon (admin), add items to cart, apply coupon code, verify discount is reflected in total. Test expired/invalid codes show clear error messages.

### Tests for User Story 4 (Write FIRST — must FAIL before implementation)

- [ ] T148 [P] [US4] Unit tests for Coupon validation rules (expiry, usage limits, minimum purchase, percentage/flat discount calculation) in services/coupon_service/tests/unit/test_entities.py
- [ ] T149 [US4] Integration tests for validate, redeem (idempotent), and admin CRUD endpoints in services/coupon_service/tests/integration/test_coupon_api.py

### Implementation for User Story 4

- [ ] T081 [P] [US4] Create coupon domain layer (Coupon entity with validation rules, CouponUsage entity, DiscountType enum, CouponRepository ABC) in services/coupon_service/coupons/domain/
- [ ] T082 [US4] Implement coupon application use cases (ValidateCoupon, RedeemCoupon idempotent, CreateCoupon, ListCoupons, UpdateCoupon, DeactivateCoupon) in services/coupon_service/coupons/application/
- [ ] T083 [US4] Create coupon Django ORM models (Coupon with unique code, CouponUsage with unique coupon+order) and generate migrations in services/coupon_service/coupons/infrastructure/models.py
- [ ] T084 [P] [US4] Implement DjangoCouponRepository in services/coupon_service/coupons/infrastructure/repositories.py
- [ ] T085 [US4] Create DRF serializers (CouponSerializer, ValidateCouponSerializer, RedeemCouponSerializer, CouponAdminSerializer) in services/coupon_service/coupons/presentation/serializers.py
- [ ] T086 [US4] Create DRF views (ValidateCouponView, RedeemCouponView, CouponAdminListCreateView, CouponAdminDetailView) in services/coupon_service/coupons/presentation/views.py
- [ ] T087 [US4] Configure coupon service URL routing (/coupons/validate, /coupons/redeem, /coupons/ admin CRUD) in services/coupon_service/coupons/presentation/urls.py and services/coupon_service/config/urls.py
- [ ] T088 [US4] Create seed data management command with sample coupons (percentage and flat, active and expired) in services/coupon_service/coupons/management/commands/seed_coupons.py

**Checkpoint**: Coupon validation and application work end-to-end through the gateway. Admin can manage coupons. Seed data available.

---

## Phase 9: User Story 5 — Place an Order and Process Payment (Priority: P2)

**Goal**: Customers checkout from cart with shipping details, pay via Stripe Checkout Sessions, receive order confirmation. Orders track full lifecycle (Pending → Confirmed → Shipped → Delivered / Cancelled). Inventory is decremented on confirmation.

**Independent Test**: Complete full purchase flow: add items to cart → proceed to checkout → enter shipping → complete Stripe payment → verify order in history with "Confirmed" status → verify confirmation email queued.

### Tests for User Story 5 (Write FIRST — must FAIL before implementation)

- [ ] T150 [P] [US5] Unit tests for Order state machine transitions (PENDING→CONFIRMED→SHIPPED→DELIVERED, CANCELLED paths) and domain event generation in services/order_service/tests/unit/test_entities.py
- [ ] T151 [US5] Integration tests for order creation orchestration, Stripe webhook, cancel, and admin status update in services/order_service/tests/integration/test_order_api.py
- [ ] T152 [P] [US5] Contract tests for cross-service HTTP clients (CartClient, ProductClient, CouponClient, RewardClient) in services/order_service/tests/contract/test_service_clients.py

### Implementation for User Story 5

- [ ] T089 [P] [US5] Create order domain layer (Order entity with status state machine, OrderItem entity, OrderRepository ABC, domain events: OrderConfirmed, OrderStatusChanged, PaymentFailed) in services/order_service/orders/domain/
- [ ] T090 [US5] Implement order application use cases (CreateOrder 6-step orchestration, ListUserOrders, GetOrderDetail, CancelOrder, HandlePaymentWebhook, AdminUpdateStatus) in services/order_service/orders/application/
- [ ] T091 [US5] Create order Django ORM models (Order with unique order_number, OrderItem with product snapshots) and generate migrations in services/order_service/orders/infrastructure/models.py
- [ ] T092 [P] [US5] Implement DjangoOrderRepository in services/order_service/orders/infrastructure/repositories.py
- [ ] T093 [US5] Implement Stripe payment integration (create Checkout Session, verify webhook signature, handle payment_intent.succeeded/failed) in services/order_service/orders/infrastructure/payment_provider.py
- [ ] T094 [P] [US5] Implement cross-service HTTP clients (CartClient, ProductClient, CouponClient for redeem, RewardClient for validate/redeem) in services/order_service/orders/infrastructure/service_clients.py
- [ ] T095 [US5] Implement order event publisher (order.order.confirmed, order.order.status_changed, order.payment.failed) in services/order_service/orders/infrastructure/event_publisher.py
- [ ] T096 [US5] Implement inventory decrement event consumer (order.confirmed → atomic stock decrement via F() expressions or SELECT FOR UPDATE; order.status_changed to CANCELLED → restore stock) in services/product_service/catalog/infrastructure/event_consumers.py
- [ ] T097 [US5] Create DRF serializers (CreateOrderSerializer with shipping fields, OrderListSerializer, OrderDetailSerializer, CancelOrderSerializer, AdminStatusUpdateSerializer) in services/order_service/orders/presentation/serializers.py
- [ ] T098 [US5] Create DRF views (CreateOrderView, OrderListView, OrderDetailView, CancelOrderView, PaymentWebhookView, AdminStatusUpdateView) in services/order_service/orders/presentation/views.py
- [ ] T099 [US5] Configure order service URL routing (/orders/*, /orders/{order_number}/cancel, /orders/webhook/payment/, /orders/{order_number}/status/) in services/order_service/orders/presentation/urls.py and services/order_service/config/urls.py
- [ ] T100 [P] [US5] Create frontend checkout page (shipping form, order summary with discounts, Stripe redirect button) in frontend/src/app/checkout/page.tsx
- [ ] T101 [P] [US5] Create frontend order history page and order detail page in frontend/src/app/orders/page.tsx and frontend/src/app/orders/[orderNumber]/page.tsx
- [ ] T102 [P] [US5] Create frontend payment callback pages (success confirmation, failure with retry option) in frontend/src/app/checkout/success/page.tsx and frontend/src/app/checkout/failure/page.tsx

**Checkpoint**: Full purchase flow works end-to-end — cart → checkout → Stripe payment → order confirmed → inventory decremented → events published.

---

## Phase 10: User Story 6 — Reward Points Program (Priority: P3)

**Goal**: Customers earn 1 reward point per $1 spent on orders. They can view balance and history, and redeem points for discounts ($0.10/point, minimum 50 points) on future orders. Points expire after 12 months.

**Independent Test**: Complete a purchase, verify points are credited to reward account, start new order and redeem points as discount, verify balance decreases.

### Tests for User Story 6 (Write FIRST — must FAIL before implementation)

- [ ] T153 [P] [US6] Unit tests for RewardAccount point calculations, minimum 50-point redemption, $0.10/point conversion, and 12-month expiration in services/reward_service/tests/unit/test_entities.py
- [ ] T154 [US6] Integration tests for reward summary, transaction history, validate-redemption, redeem endpoints, and order.confirmed consumer in services/reward_service/tests/integration/test_reward_api.py

### Implementation for User Story 6

- [ ] T103 [P] [US6] Create reward domain layer (RewardAccount entity, RewardTransaction entity, TransactionType enum, RewardRepository ABC, redemption rules: min 50 points, $0.10/point) in services/reward_service/rewards/domain/
- [ ] T104 [US6] Implement reward application use cases (GetAccountSummary, GetTransactionHistory, ValidateRedemption, RedeemPoints, CreditPoints, ExpirePoints) in services/reward_service/rewards/application/
- [ ] T105 [US6] Create reward Django ORM models (RewardAccount with unique user_id, RewardTransaction with idempotency constraint on account+order+type) and generate migrations in services/reward_service/rewards/infrastructure/models.py
- [ ] T106 [P] [US6] Implement DjangoRewardRepository in services/reward_service/rewards/infrastructure/repositories.py
- [ ] T107 [US6] Implement order.confirmed event consumer (credit 1 point per $1 of order total, set expires_at = creation + 12 months) in services/reward_service/rewards/infrastructure/event_consumers.py
- [ ] T108 [P] [US6] Implement reward event publisher (reward.points.earned with user_id, email, points, new_balance) in services/reward_service/rewards/infrastructure/event_publisher.py
- [ ] T109 [US6] Implement nightly points expiration batch job (find EARNED transactions past expires_at, create EXPIRED transactions, decrement balance) in services/reward_service/rewards/infrastructure/expiration_job.py
- [ ] T110 [US6] Create DRF serializers (RewardSummarySerializer, TransactionSerializer, ValidateRedemptionSerializer, RedeemSerializer) in services/reward_service/rewards/presentation/serializers.py
- [ ] T111 [US6] Create DRF views (RewardSummaryView, TransactionHistoryView, ValidateRedemptionView, RedeemPointsView) in services/reward_service/rewards/presentation/views.py
- [ ] T112 [US6] Configure reward service URL routing (/rewards/, /rewards/transactions/, /rewards/validate-redemption, /rewards/redeem) in services/reward_service/rewards/presentation/urls.py and services/reward_service/config/urls.py
- [ ] T113 [P] [US6] Create frontend rewards dashboard page (current balance, points expiring soon, transaction history table, redemption section) in frontend/src/app/rewards/page.tsx

**Checkpoint**: Reward points are earned on purchase, viewable on dashboard, and redeemable at checkout. Nightly expiration job is configured.

---

## Phase 11: User Story 7 — Transactional Email Notifications (Priority: P3)

**Goal**: System sends asynchronous email notifications for registration, password reset, order confirmation, order status updates, payment failures, and reward milestones. Emails retry 3x with exponential backoff and dead-letter after exhaustion.

**Independent Test**: Trigger each event (register, place order, earn points) and verify the corresponding email is queued, processed, and marked as SENT. Verify retry logic on SMTP failure.

### Tests for User Story 7 (Write FIRST — must FAIL before implementation)

- [ ] T155 [P] [US7] Unit tests for email template selection, retry orchestration logic, and dead-letter transition in services/email_service/tests/unit/test_use_cases.py
- [ ] T156 [US7] Integration tests for all 6 event consumers and SMTP provider adapter (console backend) in services/email_service/tests/integration/test_email_consumers.py

### Implementation for User Story 7

- [ ] T114 [P] [US7] Create email domain layer (EmailMessage entity, TemplateType enum: REGISTRATION/PASSWORD_RESET/ORDER_CONFIRMATION/ORDER_STATUS_UPDATE/PAYMENT_FAILED/REWARD_MILESTONE, EmailRepository ABC) in services/email_service/emails/domain/
- [ ] T115 [US7] Implement email application use cases (ProcessEventEmail, SendEmail with retry orchestration, RetryFailedEmail) in services/email_service/emails/application/
- [ ] T116 [US7] Create email Django ORM model (EmailMessage with status transitions, retry_count, event_id uniqueness) and generate migrations in services/email_service/emails/infrastructure/models.py
- [ ] T117 [P] [US7] Implement DjangoEmailRepository in services/email_service/emails/infrastructure/repositories.py
- [ ] T118 [US7] Implement SMTP email provider adapter (SendGrid/Mailgun/console backend for dev) with exponential backoff (30s→120s→480s) in services/email_service/emails/infrastructure/smtp_provider.py
- [ ] T119 [US7] Implement all 6 event consumers (user.registered, user.password_reset_requested, order.confirmed, order.status_changed, payment.failed, reward.points_earned) in services/email_service/emails/infrastructure/event_consumers.py
- [ ] T120 [P] [US7] Create email templates (plain text + HTML) for each TemplateType in services/email_service/emails/infrastructure/templates/
- [ ] T121 [US7] Create admin DRF views (EmailListView with status filter, EmailRetryView for dead-letter recovery) in services/email_service/emails/presentation/views.py
- [ ] T122 [US7] Configure email service URL routing (/emails/ admin list, /emails/{id}/retry) in services/email_service/emails/presentation/urls.py and services/email_service/config/urls.py

**Checkpoint**: All 6 transactional email types are triggered by events and delivered asynchronously. Retry and dead-letter flows work correctly.

---

## Phase 12: User Story 8 — Admin Product Management (Priority: P3)

**Goal**: Administrators create, update, and delete products and categories, manage inventory levels, and manage coupons and orders. Changes reflect on the storefront.

> **Cross-reference**: Backend coupon admin API already implemented in US4 (T082-T087). Backend order API in US5 (T090-T099). This phase adds admin-specific product use cases and all **frontend admin UI** pages.

**Independent Test**: Log in as admin, create a new product, verify it appears on storefront, update price, verify change, attempt to delete product with pending orders (expect rejection).

### Tests for User Story 8 (Write FIRST — must FAIL before implementation)

- [ ] T157 [US8] Integration tests for admin product CRUD (create, update, delete/deactivate with pending order guard) and category management in services/product_service/tests/integration/test_admin_api.py

### Implementation for User Story 8

- [ ] T123 [US8] Implement admin product use cases (CreateProduct, UpdateProduct, DeleteOrDeactivateProduct with pending order check, ManageCategories, UpdateInventory) in services/product_service/catalog/application/admin_use_cases.py
- [ ] T124 [US8] Create admin DRF serializers (ProductCreateSerializer, ProductUpdateSerializer, CategoryCreateUpdateSerializer) in services/product_service/catalog/presentation/admin_serializers.py
- [ ] T125 [US8] Create admin DRF views (ProductAdminListCreateView, ProductAdminDetailView, CategoryAdminListCreateView, CategoryAdminDetailView) in services/product_service/catalog/presentation/admin_views.py
- [ ] T126 [P] [US8] Create frontend admin layout with sidebar navigation (Products, Coupons, Orders, Dashboard) and role guard in frontend/src/app/admin/layout.tsx
- [ ] T127 [P] [US8] Create frontend admin product management pages (product list table, create form, edit form, delete confirmation) in frontend/src/app/admin/products/
- [ ] T128 [P] [US8] Create frontend admin coupon management pages (coupon list, create form, edit form, toggle active) in frontend/src/app/admin/coupons/
- [ ] T129 [P] [US8] Create frontend admin order management pages (order list with status filter, order detail, status update form) in frontend/src/app/admin/orders/
- [ ] T130 [US8] Create frontend admin dashboard with overview metrics (total orders, revenue, active products, active coupons) in frontend/src/app/admin/page.tsx

**Checkpoint**: Admin can fully manage products, coupons, and orders via the admin interface. Role-based access enforced.

---

## Phase 13: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements, documentation, security hardening, and deployment readiness.

- [ ] T131 [P] Finalize docker-compose.yml with health checks, restart policies, named volumes, and proper networking in docker-compose.yml
- [ ] T132 [P] Create docker-compose.prod.yml with production overrides (resource limits, replica counts, no debug) in docker-compose.prod.yml
- [ ] T133 [P] Add OpenAPI/Swagger auto-generation per service using drf-spectacular in services/*/config/settings.py (markdown contracts satisfy Principle V pre-implementation; machine-readable OpenAPI is a polish step)
- [ ] T134 [P] Create seed data management commands for all remaining services (admin user, sample orders) in services/*/management/commands/
- [ ] T135 Security hardening: HTTPS enforcement, CSRF protection, Secure cookie flags, input sanitization, SQL injection prevention audit across all services
- [ ] T136 [P] Add Redis caching layer for product catalog (list/detail) and coupon validation in services/product_service/ and services/coupon_service/
- [ ] T137 Validate quickstart.md flow end-to-end (docker compose up → migrations → seed → register → browse → purchase → verify email + rewards)
- [ ] T138 Update project README.md with final architecture diagram, API documentation links, and deployment guide
- [ ] T158 [P] Create Kubernetes Helm chart base with HPA auto-scaling configuration per service to satisfy FR-046 in deploy/helm/
- [ ] T159 Run load tests (locust or k6) validating SC-002 (1000 users, <200ms p95), SC-003 (<2s search), SC-009 (<1s coupon), SC-010 (<30s rewards) in tests/load/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) completion — **BLOCKS all user stories**
- **US9 — Gateway (Phase 3)**: Depends on Phase 2 — needed for all frontend-to-backend routing
- **US1 — Auth (Phase 4)**: Depends on Phase 2 — can run **in parallel** with US9
- **US2 — Products (Phase 5)**: Depends on Phase 2 — can run **in parallel** with US9 and US1
- **US10 — Messaging (Phase 6)**: Depends on Phase 2 — enables async event flows for P2/P3 stories
- **US3 — Cart (Phase 7)**: Depends on US9 (routing), US1 (auth), US2 (product data)
- **US4 — Coupons (Phase 8)**: Depends on US9 (routing), US1 (auth) — can run **in parallel** with US3
- **US5 — Orders (Phase 9)**: Depends on US3 (cart), US4 (coupons), US10 (events)
- **US6 — Rewards (Phase 10)**: Depends on US5 (order events), US10 (message bus)
- **US7 — Email (Phase 11)**: Depends on US10 (message bus) — can run **in parallel** with US6
- **US8 — Admin (Phase 12)**: Depends on US1 (admin auth), US2 (product models), US4 (coupon models)
- **Polish (Phase 13)**: Depends on all desired user stories being complete

### Dependency Graph

```
Phase 1: Setup
    │
    ▼
Phase 2: Foundational
    │
    ├──────────────────────────────────────────────┐
    │                                              │
    ▼                                              ▼
Phase 3: US9 (Gateway) ──┐     Phase 6: US10 (Messaging)
Phase 4: US1 (Auth) ─────┤              │
Phase 5: US2 (Products) ─┤              │
    [P1 — run in parallel]│              │
    │                     │              │
    ▼                     ▼              ▼
Phase 7: US3 (Cart) ◄────┘    Phase 8: US4 (Coupons)
    │                              │
    ▼                              ▼
Phase 9: US5 (Orders) ◄───────────┘
    │
    ├──────────────┐
    ▼              ▼
Phase 10: US6    Phase 11: US7 (Email)
(Rewards)          [can run in parallel]
    │              │
    ▼              ▼
Phase 12: US8 (Admin) ◄── depends on US1, US2, US4
    │
    ▼
Phase 13: Polish
```

### Within Each User Story

1. **Domain layer** first (entities, value objects, repository interfaces) — ZERO Django imports
2. **Application layer** (use cases depending on domain interfaces)
3. **Infrastructure layer** (ORM models, repository implementations, external integrations)
4. **Presentation layer** (DRF serializers, views, URL routing)
5. **Frontend** pages and components
6. Integration and wiring

### Parallel Opportunities

- **Phase 1**: T002-T004, T006-T008, T010 can all run in parallel after T001
- **Phase 2**: All [P] tasks (T012-T017, T019-T027) can run in parallel once T011 completes
- **Phases 3-5**: US9, US1, US2 can start simultaneously after Phase 2 (different services, no file conflicts)
- **Phases 7-8**: US3 (Cart) and US4 (Coupons) can run in parallel
- **Phases 10-11**: US6 (Rewards) and US7 (Email) can run in parallel after US5/US10
- **Within any story**: Domain layer [P] tasks can run in parallel; frontend [P] tasks can run in parallel

---

## Parallel Example: User Story 1 (Auth)

```bash
# Step 1: Domain layer (T039) — all domain files in one task
Task: "Create auth domain layer" → services/auth_service/auth/domain/

# Step 2: Application layer (T040) — depends on T039
Task: "Implement auth application use cases" → services/auth_service/auth/application/

# Step 3: Infrastructure — T041 first, then T042-T044 in parallel
Task: "Create auth ORM models" (T041)
Task [P]: "Implement DjangoUserRepository" (T042)
Task [P]: "Implement JWT provider" (T043)
Task: "Implement event publisher" (T044) — depends on shared message_bus

# Step 4: Presentation — sequential within layer
Task: "Create DRF serializers" (T045)
Task: "Create DRF views" (T046)
Task: "Configure URL routing" (T047)

# Step 5: Frontend — T048-T050 in parallel, then T051
Task [P]: "Create login page" (T048)
Task [P]: "Create register page" (T049)
Task [P]: "Create forgot-password pages" (T050)
Task: "Wire auth forms to API client" (T051)
```

---

## Implementation Strategy

### MVP First (P1 Stories Only)

1. Complete Phase 1: Setup (10 tasks)
2. Complete Phase 2: Foundational — **CRITICAL, blocks all stories** (18 tasks)
3. Complete Phases 3-5: US9 + US1 + US2 in parallel (35 tasks)
4. **STOP and VALIDATE**: Gateway + Auth + Products working end-to-end
5. Deploy/demo MVP: users can register, browse, and search products

### Incremental Delivery

1. **Foundation** (Phases 1-2) → Infrastructure ready → 28 tasks
2. **MVP** (Phases 3-5) → Gateway + Auth + Products → 41 tasks → First deployment
3. **Commerce** (Phases 6-9) → Messaging + Cart + Coupons + Orders → 47 tasks → Full purchase flow
4. **Loyalty** (Phases 10-11) → Rewards + Email → 24 tasks → Enhanced experience
5. **Operations** (Phases 12-13) → Admin + Polish → 19 tasks → Production ready

### Suggested MVP Scope

**Minimum MVP** (Phases 1-5): 69 tasks
- Delivers: User registration, authentication, product catalog with search/filtering
- Value: Users can register, browse products, and experience the platform core

**Extended MVP** (Phases 1-9): 116 tasks
- Delivers: Full purchase flow with cart, coupons, orders, and payment
- Value: Complete e-commerce transaction capability

**Full Platform** (Phases 1-13): 159 tasks
- Delivers: Rewards, email notifications, admin management, production readiness
- Value: Feature-complete platform ready for production deployment

---

## Notes

- **[P] tasks** = different files, no dependencies on in-progress tasks
- **[USx] label** maps each task to a specific user story for traceability
- Each user story is independently completable and testable at its checkpoint
- **Domain layer** has ZERO Django imports — pure Python dataclasses and ABCs
- All **cross-service references** use opaque UUIDs (no foreign keys across services)
- **Commit** after each task or logical group
- Stop at any **checkpoint** to validate the completed story independently
- Constitution Principle III (Test-First Development) is satisfied with test tasks T139-T157 written BEFORE implementation in each phase
- SC-005 (90% first-purchase success rate) is a UX metric measured via production analytics, not automated testing
- Avoid: vague tasks, same-file conflicts across parallel tasks, cross-story dependencies that break independence
