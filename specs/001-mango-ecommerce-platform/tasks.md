# Tasks: Mango Microservices E-Commerce Platform

**Input**: Design documents from `/specs/001-mango-ecommerce-platform/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Included. The specification and constitution require test-first delivery, so each user story contains test tasks that should be written and made to fail before implementation.

**Organization**: Tasks are grouped by user story so each slice can be implemented and validated independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Parallelizable task with no dependency on another incomplete task in the same phase
- **[Story]**: User story label (`[US1]`, `[US2]`, etc.)
- Every task includes exact file paths or target directories

---

## Phase 1: Setup

**Purpose**: Align the repository structure, environment files, and container/runtime scaffolding with the implementation plan.

- [X] T001 Align local development orchestration for all services, frontend, PostgreSQL, RabbitMQ, and Redis in docker-compose.yml
- [X] T002 [P] Add shared environment templates for root and each service in .env.example, services/auth_service/.env.example, services/product_service/.env.example, services/cart_service/.env.example, services/coupon_service/.env.example, services/order_service/.env.example, services/reward_service/.env.example, services/email_service/.env.example, and services/gateway/.env.example
- [X] T003 [P] Create missing shared utility package structure in shared/common/__init__.py, shared/common/config.py, and shared/common/logging_config.py
- [X] T004 [P] Create missing layer package scaffolding for cart, coupon, order, reward, email, and gateway services in services/cart_service/cart/application/__init__.py, services/cart_service/cart/infrastructure/__init__.py, services/cart_service/cart/presentation/__init__.py, services/coupon_service/coupons/application/__init__.py, services/coupon_service/coupons/infrastructure/__init__.py, services/coupon_service/coupons/presentation/__init__.py, services/order_service/orders/application/__init__.py, services/order_service/orders/infrastructure/__init__.py, services/order_service/orders/presentation/__init__.py, services/reward_service/rewards/application/__init__.py, services/reward_service/rewards/infrastructure/__init__.py, services/reward_service/rewards/presentation/__init__.py, services/email_service/emails/application/__init__.py, services/email_service/emails/infrastructure/__init__.py, services/email_service/emails/presentation/__init__.py, services/gateway/gateway/application/__init__.py, services/gateway/gateway/domain/__init__.py, services/gateway/gateway/infrastructure/__init__.py, and services/gateway/gateway/presentation/__init__.py
- [X] T005 [P] Standardize Python dependency declarations for shared libraries, Celery, DRF, Redis, and pytest across services in pyproject.toml, services/auth_service/pyproject.toml, services/product_service/pyproject.toml, services/cart_service/pyproject.toml, services/coupon_service/pyproject.toml, services/order_service/pyproject.toml, services/reward_service/pyproject.toml, services/email_service/pyproject.toml, and services/gateway/pyproject.toml
- [X] T006 [P] Align frontend workspace scripts and dependencies for Next.js testing and linting in frontend/package.json and pnpm-workspace.yaml
- [X] T007 [P] Update service and frontend container build definitions in services/auth_service/Dockerfile, services/product_service/Dockerfile, services/cart_service/Dockerfile, services/coupon_service/Dockerfile, services/order_service/Dockerfile, services/reward_service/Dockerfile, services/email_service/Dockerfile, services/gateway/Dockerfile, and frontend/Dockerfile
- [X] T008 Add repository quickstart and architecture entrypoints to README.md and confirm the launch sequence remains consistent with specs/001-mango-ecommerce-platform/quickstart.md

---

## Phase 2: Foundational

**Purpose**: Build shared infrastructure that blocks all user stories until complete.

**⚠️ CRITICAL**: No user story work should start until this phase is finished.

- [X] T009 Implement the shared event envelope and typed base event contracts in shared/message_bus/events.py
- [X] T010 [P] Implement message publishing with durable routing-key support in shared/message_bus/bus.py and shared/message_bus/publisher.py
- [X] T011 [P] Implement idempotent consumer helpers, retry policy, and dead-letter routing support in shared/message_bus/consumer.py and shared/message_bus/dlq.py
- [X] T012 [P] Implement shared exception and response helpers in shared/common/exceptions.py and shared/common/responses.py
- [X] T013 [P] Implement shared configuration loading and structured logging helpers in shared/common/config.py and shared/common/logging_config.py
- [X] T014 [P] Configure Django settings, DRF defaults, Redis, and Celery bootstrap across services in services/auth_service/auth_service/settings.py, services/product_service/product_service/settings.py, services/cart_service/cart_service/settings.py, services/coupon_service/coupon_service/settings.py, services/order_service/order_service/settings.py, services/reward_service/reward_service/settings.py, services/email_service/email_service/settings.py, services/gateway/gateway/settings.py, services/auth_service/auth_service/celery.py, services/product_service/product_service/celery.py, services/cart_service/cart_service/celery.py, services/coupon_service/coupon_service/celery.py, services/order_service/order_service/celery.py, services/reward_service/reward_service/celery.py, services/email_service/email_service/celery.py, and services/gateway/gateway/celery.py
- [X] T015 [P] Add shared health-check utilities and service health views in shared/common/health.py, services/auth_service/health.py, services/product_service/health.py, services/cart_service/health.py, services/coupon_service/health.py, services/order_service/health.py, services/reward_service/health.py, services/email_service/health.py, and services/gateway/health.py
- [X] T016 [P] Build shared pytest factories and reusable service fixtures in shared/testing/__init__.py, shared/testing/factories.py, and shared/testing/fixtures.py
- [X] T017 [P] Build the frontend API client and shared response types in frontend/src/lib/api/client.ts, frontend/src/lib/api/index.ts, and frontend/src/types/index.ts
- [X] T018 [P] Build the frontend auth/cart providers and application shell in frontend/src/lib/auth/context.tsx, frontend/src/lib/cart/context.tsx, frontend/src/components/layout/Header.tsx, frontend/src/components/layout/Footer.tsx, and frontend/src/app/layout.tsx
- [X] T118 [P] Generate and validate initial OpenAPI contracts for all gateway-exposed services before story implementation in specs/001-mango-ecommerce-platform/contracts/, services/auth_service/auth_service/settings.py, services/product_service/product_service/settings.py, services/cart_service/cart_service/settings.py, services/coupon_service/coupon_service/settings.py, services/order_service/order_service/settings.py, services/reward_service/reward_service/settings.py, services/email_service/email_service/settings.py, and services/gateway/gateway/settings.py

**Checkpoint**: Shared transport, config, logging, testing, and frontend shell are ready. Story work can now begin.

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Let customers and admins register, log in, refresh sessions, log out, and reset passwords with lockout protection and JWT-backed sessions.

**Independent Test**: Register a new user, log in, verify cookies/session state, retrieve the current profile, trigger password reset, and confirm lockout after five failed logins.

### Tests for User Story 1

- [X] T019 [P] [US1] Add domain and use-case unit tests for user validation, password rules, refresh token rotation, and lockout behavior in services/auth_service/tests/unit/test_entities.py and services/auth_service/tests/unit/test_use_cases.py
- [X] T020 [US1] Add API integration tests for register, login, refresh, logout, me, forgot-password, and reset-password flows in services/auth_service/tests/integration/test_auth_api.py

### Implementation for User Story 1

- [X] T021 [P] [US1] Implement auth domain entities, value objects, and domain events in services/auth_service/auth/domain/entities.py and services/auth_service/auth/domain/value_objects.py
- [X] T022 [US1] Implement registration, login, refresh, logout, profile, forgot-password, and reset-password use cases in services/auth_service/auth/application/use_cases/register_user.py, services/auth_service/auth/application/use_cases/login_user.py, services/auth_service/auth/application/use_cases/refresh_token.py, services/auth_service/auth/application/use_cases/logout_user.py, services/auth_service/auth/application/use_cases/get_profile.py, services/auth_service/auth/application/use_cases/forgot_password.py, and services/auth_service/auth/application/use_cases/reset_password.py
- [X] T023 [US1] Implement persistence models and migrations for users and refresh tokens in services/auth_service/auth_service/models.py and services/auth_service/auth_service/migrations/
- [X] T024 [P] [US1] Implement repository, password hashing, and token services in services/auth_service/auth/infrastructure/repositories.py, services/auth_service/auth/application/crypto.py, and services/auth_service/auth/application/jwt_utils.py
- [X] T025 [US1] Implement auth serializers and views in services/auth_service/auth/presentation/serializers.py and services/auth_service/auth/presentation/views.py
- [X] T026 [US1] Wire auth endpoints and service URLs in services/auth_service/auth/presentation/urls.py and services/auth_service/auth_service/urls.py
- [X] T027 [P] [US1] Build login, register, forgot-password, and reset-password pages in frontend/src/app/(auth)/login/page.tsx, frontend/src/app/(auth)/register/page.tsx, frontend/src/app/(auth)/forgot-password/page.tsx, and frontend/src/app/(auth)/reset-password/page.tsx
- [X] T028 [US1] Connect frontend auth pages to the shared API/auth context and protected-route behavior in frontend/src/lib/auth/context.tsx and frontend/src/components/layout/Header.tsx
- [X] T119 [US1] Implement and verify registration/password-reset email delivery path required by US1 acceptance in services/auth_service/auth/infrastructure/event_publisher.py, services/email_service/emails/infrastructure/event_consumers.py, and services/email_service/emails/infrastructure/templates/
- [X] T120 [US1] Add integration coverage for registration/password-reset side effects (email queued and sent) in services/auth_service/tests/integration/test_auth_email_flow.py and services/email_service/tests/integration/test_auth_events.py

**Checkpoint**: Registration, login, session refresh, logout, profile lookup, and password reset work end to end.

---

## Phase 4: User Story 2 - Browse and Search Product Catalog (Priority: P1) 🎯 MVP

**Goal**: Expose a searchable, filterable product catalog with category browsing and product detail pages.

**Independent Test**: Load the storefront, search by keyword, filter by category and stock, and open a product detail page.

### Tests for User Story 2

- [X] T029 [P] [US2] Add unit tests for product/category entities, pricing, stock state, and filter logic in services/product_service/tests/unit/test_entities.py and services/product_service/tests/unit/test_catalog_filters.py
- [X] T030 [US2] Add integration tests for catalog listing, search, category tree, and product detail endpoints in services/product_service/tests/integration/test_product_api.py

### Implementation for User Story 2

- [X] T031 [P] [US2] Implement product and category domain models and repository contracts in services/product_service/catalog/domain/entities.py and services/product_service/catalog/domain/repositories.py
- [X] T032 [US2] Implement list/search/detail/category application use cases in services/product_service/catalog/application/use_cases/list_products.py, services/product_service/catalog/application/use_cases/search_products.py, services/product_service/catalog/application/use_cases/get_product_detail.py, and services/product_service/catalog/application/use_cases/list_categories.py
- [X] T033 [US2] Implement catalog persistence models and migrations in services/product_service/catalog/models.py and services/product_service/migrations/
- [X] T034 [P] [US2] Implement catalog repository and full-text search behavior in services/product_service/catalog/infrastructure/repositories.py
- [X] T035 [US2] Implement product and category serializers and read-only views in services/product_service/catalog/presentation/serializers.py and services/product_service/catalog/presentation/views.py
- [X] T036 [US2] Wire public and internal product routes in services/product_service/catalog/presentation/urls.py and services/product_service/product_service/urls.py
- [X] T037 [P] [US2] Build the product listing and product detail pages in frontend/src/app/products/page.tsx and frontend/src/app/products/[slug]/page.tsx
- [X] T038 [US2] Build reusable catalog UI pieces and search/filter controls in frontend/src/components/products/ProductCard.tsx, frontend/src/components/products/ProductGrid.tsx, and frontend/src/components/products/ProductFilters.tsx

**Checkpoint**: Customers can browse, search, filter, and inspect products through the gateway-backed frontend.

---

## Phase 5: User Story 9 - API Gateway Routing and Cross-Cutting Concerns (Priority: P1) 🎯 MVP

**Goal**: Route all frontend API traffic through a single gateway that validates authentication, injects user context, enforces rate limits, and normalizes errors.

**Independent Test**: Send requests to `/api/v1/*` routes and verify correct upstream routing, 401 handling for protected routes, 429 handling for rate limits, and 503 handling for unavailable services.

### Tests for User Story 9

- [X] T039 [P] [US9] Add gateway unit tests for route matching, JWT validation, and rate-limit rules in services/gateway/tests/unit/test_routes.py, services/gateway/tests/unit/test_jwt_validator.py, and services/gateway/tests/unit/test_rate_limiter.py
- [X] T040 [US9] Add gateway integration tests for proxy forwarding, auth rejection, upstream failure handling, and header injection in services/gateway/tests/integration/test_proxy.py

### Implementation for User Story 9

- [X] T041 [P] [US9] Implement route maps and rate-limit definitions in services/gateway/gateway/domain/routes.py and services/gateway/gateway/domain/rate_limits.py
- [X] T042 [US9] Implement proxy orchestration and service health aggregation use cases in services/gateway/gateway/application/proxy_request.py and services/gateway/gateway/application/health_summary.py
- [X] T043 [P] [US9] Implement async upstream HTTP client and service registry helpers in services/gateway/gateway/infrastructure/http_client.py and services/gateway/routing.py
- [X] T044 [P] [US9] Implement JWT validation and Redis-backed throttling services in services/gateway/gateway/infrastructure/jwt_validator.py and services/gateway/gateway/infrastructure/rate_limiter.py
- [X] T045 [US9] Implement request middleware for correlation ID, auth, throttling, and logging in services/gateway/gateway/presentation/middleware/request_context.py and services/gateway/gateway/presentation/middleware/auth.py
- [X] T046 [US9] Implement gateway proxy and health views in services/gateway/gateway/presentation/views.py
- [X] T047 [US9] Wire gateway URLs and upstream route exposure in services/gateway/gateway/presentation/urls.py and services/gateway/gateway/urls.py
- [X] T048 [US9] Point the frontend API base configuration to the gateway and handle normalized gateway errors in frontend/src/lib/api/client.ts and frontend/src/types/index.ts

**Checkpoint**: The frontend talks only to the gateway, and the gateway correctly handles routing, auth, rate limiting, and service errors.

---

## Phase 6: User Story 3 - Shopping Cart Management (Priority: P2)

**Goal**: Let authenticated users maintain a persistent cart, update quantities, remove items, and preview coupon effects.

**Independent Test**: Add items to cart, update quantities, remove an item, log out and back in, and confirm the cart is preserved.

### Tests for User Story 3

- [ ] T049 [P] [US3] Add cart domain and use-case unit tests for quantity validation, subtotal calculation, and cart limits in services/cart_service/tests/unit/test_entities.py and services/cart_service/tests/unit/test_use_cases.py
- [ ] T050 [US3] Add cart integration tests for get/add/update/remove/apply-coupon/remove-coupon flows in services/cart_service/tests/integration/test_cart_api.py

### Implementation for User Story 3

- [ ] T051 [P] [US3] Implement cart and cart-item domain models and repository contracts in services/cart_service/cart/domain/entities.py and services/cart_service/cart/domain/repositories.py
- [ ] T052 [US3] Implement cart use cases in services/cart_service/cart/application/use_cases/get_cart.py, services/cart_service/cart/application/use_cases/add_item.py, services/cart_service/cart/application/use_cases/update_item.py, services/cart_service/cart/application/use_cases/remove_item.py, services/cart_service/cart/application/use_cases/clear_cart.py, services/cart_service/cart/application/use_cases/apply_coupon.py, and services/cart_service/cart/application/use_cases/remove_coupon.py
- [ ] T053 [US3] Implement cart persistence models and migrations in services/cart_service/cart_service/models.py and services/cart_service/migrations/
- [ ] T054 [P] [US3] Implement cart repository and upstream product/coupon clients in services/cart_service/cart/infrastructure/repositories.py, services/cart_service/cart/infrastructure/product_client.py, and services/cart_service/cart/infrastructure/coupon_client.py
- [ ] T055 [US3] Implement cart serializers and views in services/cart_service/cart/presentation/serializers.py and services/cart_service/cart/presentation/views.py
- [ ] T056 [US3] Wire cart endpoints in services/cart_service/cart/presentation/urls.py and services/cart_service/cart_service/urls.py
- [ ] T057 [P] [US3] Build the cart page and cart drawer UI in frontend/src/app/cart/page.tsx, frontend/src/components/cart/CartDrawer.tsx, and frontend/src/components/cart/CartItemRow.tsx
- [ ] T058 [US3] Connect product pages and cart UI to the shared cart context in frontend/src/lib/cart/context.tsx and frontend/src/app/products/[slug]/page.tsx

**Checkpoint**: Cart CRUD, persistence, and subtotal updates work across sessions.

---

## Phase 7: User Story 4 - Apply Coupons and Discounts (Priority: P2)

**Goal**: Support coupon validation and redemption with admin coupon management.

**Independent Test**: Create a coupon as admin, apply it to a cart or order subtotal, and verify correct discount or validation errors.

### Tests for User Story 4

- [ ] T059 [P] [US4] Add coupon domain and discount-calculation unit tests in services/coupon_service/tests/unit/test_entities.py and services/coupon_service/tests/unit/test_discount_rules.py
- [ ] T060 [US4] Add integration tests for validate, redeem, and admin coupon CRUD endpoints in services/coupon_service/tests/integration/test_coupon_api.py

### Implementation for User Story 4

- [ ] T061 [P] [US4] Implement coupon and coupon-usage domain models and repository contracts in services/coupon_service/coupons/domain/entities.py and services/coupon_service/coupons/domain/repositories.py
- [ ] T062 [US4] Implement validate, redeem, create, update, list, and deactivate coupon use cases in services/coupon_service/coupons/application/use_cases/validate_coupon.py, services/coupon_service/coupons/application/use_cases/redeem_coupon.py, services/coupon_service/coupons/application/use_cases/create_coupon.py, services/coupon_service/coupons/application/use_cases/update_coupon.py, and services/coupon_service/coupons/application/use_cases/list_coupons.py
- [ ] T063 [US4] Implement coupon persistence models and migrations in services/coupon_service/coupon_service/models.py and services/coupon_service/migrations/
- [ ] T064 [P] [US4] Implement coupon repository logic and idempotent redemption checks in services/coupon_service/coupons/infrastructure/repositories.py
- [ ] T065 [US4] Implement coupon serializers and views for validation, redemption, and admin CRUD in services/coupon_service/coupons/presentation/serializers.py and services/coupon_service/coupons/presentation/views.py
- [ ] T066 [US4] Wire coupon endpoints in services/coupon_service/coupons/presentation/urls.py and services/coupon_service/coupon_service/urls.py
- [ ] T067 [US4] Add coupon seed command for development and quickstart validation in services/coupon_service/coupons/infrastructure/management/commands/seed_coupons.py

**Checkpoint**: Coupon validation, redemption, and admin management are complete.

---

## Phase 8: User Story 10 - Asynchronous Inter-Service Messaging (Priority: P2)

**Goal**: Provide durable event publishing and idempotent consumption across order, email, reward, and product flows.

**Independent Test**: Publish an order confirmation event and verify consumers process it once, retries occur on failure, and unrecoverable messages land in the DLQ.

### Tests for User Story 10

- [ ] T068 [US10] Add message-bus integration tests for publish/consume, retry, idempotency, and dead-letter behavior in shared/testing/test_message_bus.py

### Implementation for User Story 10

- [ ] T069 [US10] Implement contract-specific domain event classes and payload serializers in shared/message_bus/events.py
- [ ] T070 [P] [US10] Implement RabbitMQ exchange, queue-binding, and routing-key configuration in shared/message_bus/config.py and shared/message_bus/bindings.py
- [ ] T071 [P] [US10] Add processed-event persistence and idempotency bookkeeping in services/product_service/catalog/infrastructure/processed_events.py, services/reward_service/rewards/infrastructure/processed_events.py, and services/email_service/emails/infrastructure/processed_events.py
- [ ] T072 [US10] Implement consumer registration and worker bootstrap for product, reward, and email services in services/product_service/product_service/celery.py, services/reward_service/reward_service/celery.py, and services/email_service/email_service/celery.py
- [ ] T073 [US10] Implement shared dead-letter inspection and replay helpers in shared/message_bus/dlq.py and shared/testing/fixtures.py

**Checkpoint**: The event bus is ready for order, reward, email, and inventory workflows.

---

## Phase 9: User Story 5 - Place an Order and Process Payment (Priority: P2)

**Goal**: Let users checkout from their cart, pay successfully, persist orders, update inventory, and publish follow-up events.

**Independent Test**: Complete a checkout from cart to payment confirmation, then verify order history, inventory adjustment, and event publication.

### Tests for User Story 5

- [ ] T074 [P] [US5] Add order domain unit tests for totals, discount rules, and status transitions in services/order_service/tests/unit/test_entities.py and services/order_service/tests/unit/test_status_transitions.py
- [ ] T075 [US5] Add order integration tests for create, detail, list, cancel, webhook, and admin status-update flows in services/order_service/tests/integration/test_order_api.py
- [ ] T076 [P] [US5] Add contract tests for cart, product, coupon, and reward upstream clients in services/order_service/tests/contract/test_service_clients.py

### Implementation for User Story 5

- [ ] T077 [P] [US5] Implement order and order-item domain models, status state machine, and domain events in services/order_service/orders/domain/entities.py and services/order_service/orders/domain/events.py
- [ ] T078 [US5] Implement create-order, list-orders, get-order, cancel-order, payment-webhook, and admin status-update use cases in services/order_service/orders/application/use_cases/create_order.py, services/order_service/orders/application/use_cases/list_orders.py, services/order_service/orders/application/use_cases/get_order.py, services/order_service/orders/application/use_cases/cancel_order.py, services/order_service/orders/application/use_cases/handle_payment_webhook.py, and services/order_service/orders/application/use_cases/update_order_status.py
- [ ] T079 [US5] Implement order persistence models and migrations in services/order_service/order_service/models.py and services/order_service/migrations/
- [ ] T080 [P] [US5] Implement order repository and upstream service clients in services/order_service/orders/infrastructure/repositories.py and services/order_service/orders/infrastructure/service_clients.py
- [ ] T081 [US5] Implement payment-provider integration and event publishing in services/order_service/orders/infrastructure/payment_provider.py and services/order_service/orders/infrastructure/event_publisher.py
- [ ] T082 [US5] Implement order serializers and views in services/order_service/orders/presentation/serializers.py and services/order_service/orders/presentation/views.py
- [ ] T083 [US5] Wire order endpoints and webhook routes in services/order_service/orders/presentation/urls.py and services/order_service/order_service/urls.py
- [ ] T084 [P] [US5] Build checkout, order history, and order detail pages in frontend/src/app/checkout/page.tsx, frontend/src/app/orders/page.tsx, and frontend/src/app/orders/[orderNumber]/page.tsx
- [ ] T085 [US5] Connect checkout UI to payment redirects, success/failure handling, and order retrieval in frontend/src/app/checkout/success/page.tsx, frontend/src/app/checkout/failure/page.tsx, and frontend/src/lib/api/client.ts
- [ ] T121 [US5] Implement order timeout monitor and retry/cancel flow (default 15 minutes) for pending payments in services/order_service/orders/application/use_cases/handle_order_timeout.py and services/order_service/order_service/celery.py
- [ ] T122 [US5] Implement required checkout side effects for confirmation email and reward credit on order confirmation in services/email_service/emails/infrastructure/event_consumers.py and services/reward_service/rewards/infrastructure/event_consumers.py
- [ ] T123 [US5] Add end-to-end integration test for checkout -> order confirmation -> reward credit + confirmation email in services/order_service/tests/integration/test_checkout_side_effects.py

**Checkpoint**: A complete purchase flow works and emits the required events.

---

## Phase 10: User Story 6 - Reward Points Program (Priority: P3)

**Goal**: Credit, redeem, view, and expire customer reward points based on confirmed orders.

**Independent Test**: Confirm an order, verify points are credited, then redeem points on a later order and inspect reward history.

### Tests for User Story 6

- [ ] T086 [P] [US6] Add reward-account and redemption unit tests in services/reward_service/tests/unit/test_entities.py and services/reward_service/tests/unit/test_redemption_rules.py
- [ ] T087 [US6] Add integration tests for reward summary, history, validate-redemption, redeem, and order-confirmed consumption in services/reward_service/tests/integration/test_reward_api.py

### Implementation for User Story 6

- [ ] T088 [P] [US6] Implement reward-account and reward-transaction domain models in services/reward_service/rewards/domain/entities.py and services/reward_service/rewards/domain/repositories.py
- [ ] T089 [US6] Implement reward summary, transaction history, validate-redemption, redeem-points, credit-points, and expire-points use cases in services/reward_service/rewards/application/use_cases/get_summary.py, services/reward_service/rewards/application/use_cases/list_transactions.py, services/reward_service/rewards/application/use_cases/validate_redemption.py, services/reward_service/rewards/application/use_cases/redeem_points.py, services/reward_service/rewards/application/use_cases/credit_points.py, and services/reward_service/rewards/application/use_cases/expire_points.py
- [ ] T090 [US6] Implement reward persistence models and migrations in services/reward_service/reward_service/models.py and services/reward_service/migrations/
- [ ] T091 [P] [US6] Implement reward repository, order-confirmed consumer, and reward-points-earned publisher in services/reward_service/rewards/infrastructure/repositories.py, services/reward_service/rewards/infrastructure/event_consumers.py, and services/reward_service/rewards/infrastructure/event_publisher.py
- [ ] T092 [US6] Implement reward serializers and views in services/reward_service/rewards/presentation/serializers.py and services/reward_service/rewards/presentation/views.py
- [ ] T093 [US6] Wire reward endpoints in services/reward_service/rewards/presentation/urls.py and services/reward_service/reward_service/urls.py
- [ ] T094 [US6] Build the reward dashboard and transaction UI in frontend/src/app/rewards/page.tsx and frontend/src/components/ui/RewardSummaryCard.tsx
- [ ] T124 [US6] Configure scheduled reward-point expiration (Celery beat/periodic task) for FR-032 in services/reward_service/reward_service/celery.py and services/reward_service/rewards/application/use_cases/expire_points.py

**Checkpoint**: Reward earning, redemption, history, and expiration are working.

---

## Phase 11: User Story 7 - Transactional Email Notifications (Priority: P3)

**Goal**: Send registration, password reset, order, payment-failure, reward, and status-update emails asynchronously with retries and dead-letter handling.
**Scope Note**: US1 covers auth-triggered email side effects required for early acceptance; US7 hardens and generalizes the full email platform (all event types, retries, dead-letter handling, and admin monitoring).

**Independent Test**: Trigger each supported event, verify email records are queued and sent, then force failures to confirm retries and dead-letter behavior.

### Tests for User Story 7

- [ ] T095 [P] [US7] Add email use-case and retry-policy unit tests in services/email_service/tests/unit/test_use_cases.py and services/email_service/tests/unit/test_retry_policy.py
- [ ] T096 [US7] Add integration tests for event consumers, template rendering, and admin monitoring endpoints in services/email_service/tests/integration/test_email_service.py

### Implementation for User Story 7

- [ ] T097 [P] [US7] Implement email-message domain models and repository contracts in services/email_service/emails/domain/entities.py and services/email_service/emails/domain/repositories.py
- [ ] T098 [US7] Implement email send/retry/replay use cases in services/email_service/emails/application/use_cases/process_event_email.py, services/email_service/emails/application/use_cases/send_email.py, and services/email_service/emails/application/use_cases/retry_email.py
- [ ] T099 [US7] Implement email persistence models and migrations in services/email_service/email_service/models.py and services/email_service/migrations/
- [ ] T100 [P] [US7] Implement email repository, SMTP provider, and event consumers in services/email_service/emails/infrastructure/repositories.py, services/email_service/emails/infrastructure/smtp_provider.py, and services/email_service/emails/infrastructure/event_consumers.py
- [ ] T101 [P] [US7] Add HTML and text email templates for all supported event types in services/email_service/emails/infrastructure/templates/
- [ ] T102 [US7] Implement admin serializers and monitoring views in services/email_service/emails/presentation/serializers.py and services/email_service/emails/presentation/views.py
- [ ] T103 [US7] Wire admin email endpoints in services/email_service/emails/presentation/urls.py and services/email_service/email_service/urls.py

**Checkpoint**: Transactional email delivery is asynchronous, observable, and resilient.

---

## Phase 12: User Story 8 - Admin Product Management (Priority: P3)

**Goal**: Give admins the ability to manage products, categories, coupons, and order statuses from the frontend admin area.

**Independent Test**: Log in as admin, create and edit a product, manage a coupon, update an order status, and verify storefront changes reflect correctly.

### Tests for User Story 8

- [ ] T104 [US8] Add integration tests for admin product/category management and pending-order deletion guards in services/product_service/tests/integration/test_admin_api.py

### Implementation for User Story 8

- [ ] T105 [US8] Implement admin product/category application use cases in services/product_service/catalog/application/use_cases/admin_create_product.py, services/product_service/catalog/application/use_cases/admin_update_product.py, services/product_service/catalog/application/use_cases/admin_delete_product.py, and services/product_service/catalog/application/use_cases/admin_manage_category.py
- [ ] T106 [US8] Implement admin serializers and views for product/category management in services/product_service/catalog/presentation/admin_serializers.py and services/product_service/catalog/presentation/admin_views.py
- [ ] T107 [US8] Wire admin product/category routes in services/product_service/catalog/presentation/admin_urls.py and services/product_service/product_service/urls.py
- [ ] T108 [P] [US8] Build the admin shell and dashboard in frontend/src/app/admin/layout.tsx and frontend/src/app/admin/page.tsx
- [ ] T109 [P] [US8] Build admin product management pages in frontend/src/app/admin/products/page.tsx, frontend/src/app/admin/products/new/page.tsx, and frontend/src/app/admin/products/[id]/page.tsx
- [ ] T110 [P] [US8] Build admin coupon management pages in frontend/src/app/admin/coupons/page.tsx and frontend/src/app/admin/coupons/[id]/page.tsx
- [ ] T111 [US8] Build admin order management pages in frontend/src/app/admin/orders/page.tsx and frontend/src/app/admin/orders/[orderNumber]/page.tsx

**Checkpoint**: Admins can manage operational catalog, coupon, and order workflows from the UI.

---

## Phase 13: Polish & Cross-Cutting Concerns

**Purpose**: Finalize documentation, performance, security, and deployment readiness across the completed stories.

- [ ] T112 [P] Add OpenAPI generation and API schema publishing for each backend service in services/auth_service/auth_service/settings.py, services/product_service/product_service/settings.py, services/cart_service/cart_service/settings.py, services/coupon_service/coupon_service/settings.py, services/order_service/order_service/settings.py, services/reward_service/reward_service/settings.py, services/email_service/email_service/settings.py, and services/gateway/gateway/settings.py
- [ ] T113 [P] Add caching and performance tuning for product catalog and coupon validation in services/product_service/catalog/infrastructure/repositories.py and services/coupon_service/coupons/infrastructure/repositories.py
- [ ] T114 Harden cookies, CSRF, HTTPS, input validation, and service-to-service auth settings in services/auth_service/auth_service/settings.py, services/gateway/gateway/settings.py, and shared/common/config.py
- [ ] T115 [P] Add load and smoke test coverage with explicit pass thresholds: SC-002 (1000 concurrent users, <200ms p95 catalog API), SC-003 (95% of search queries <2s), SC-009 (coupon validation <1s), and SC-010 (reward credit <30s) in testing/load/test_catalog.py, testing/load/test_checkout.py, and testing/smoke/test_quickstart_flow.py
- [ ] T116 Validate the documented startup flow and seed commands against specs/001-mango-ecommerce-platform/quickstart.md and update README.md with the verified commands and architecture summary
- [ ] T117 [P] Add deployment scaffolding for horizontal scaling targets in docker-compose.yml, docker/docker-compose.prod.yml, and deploy/helm/
- [ ] T125 [P] Add funnel analytics instrumentation and reporting for first-purchase success (SC-005) in frontend/src/lib/analytics/funnel.ts, frontend/src/app/checkout/success/page.tsx, and shared/testing/fixtures.py
- [ ] T126 Add automated KPI validation for SC-005 in testing/smoke/test_first_purchase_success.py and README.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1: Setup** has no dependencies.
- **Phase 2: Foundational** depends on Phase 1 and blocks all story work (including OpenAPI baseline task T118).
- **Phase 3: US1**, **Phase 4: US2**, and **Phase 5: US9** can start after Phase 2 and may proceed in parallel.
- **Phase 6: US3** depends on US1, US2, and US9.
- **Phase 7: US4** depends on US1 and US9.
- **Phase 8: US10** depends on Phase 2 and should finish before event-driven downstream stories rely on it.
- **Phase 9: US5** depends on US3, US4, and US10.
- **Phase 10: US6** depends on US5 and US10.
- **Phase 11: US7** depends on US1, US5, and US10.
- **Phase 12: US8** depends on US1, US2, US4, and US5.
- **Phase 13: Polish** depends on all desired user stories being complete.

### User Story Dependency Graph

```text
Setup -> Foundational
Foundational -> US1, US2, US9, US10
US1 + US2 + US9 -> US3
US1 + US9 -> US4
US3 + US4 + US10 -> US5
US5 + US10 -> US6
US1 + US5 + US10 -> US7
US1 + US2 + US4 + US5 -> US8
All complete -> Polish
```

### Parallel Opportunities

- **US1**: T021 and T023 can proceed in parallel after tests are written.
- **US2**: T031 and T033 can proceed in parallel after tests are written.
- **US9**: T041, T043, and T044 can proceed in parallel after tests are written.
- **US3**: T051 and T053 can proceed in parallel after tests are written.
- **US4**: T061 and T063 can proceed in parallel after tests are written.
- **US10**: T070 and T071 can proceed in parallel after T069.
- **US5**: T077, T079, and T080 can proceed in parallel after tests are written.
- **US6**: T088 and T090 can proceed in parallel after tests are written.
- **US7**: T097, T099, and T101 can proceed in parallel after tests are written.
- **US8**: T108, T109, and T110 can proceed in parallel after T105-T107 are settled.
- **Polish**: T125 and T117 can proceed in parallel after core stories are complete.

---

## Parallel Execution Examples

- **US1**: Run T021, T023, and T027 in parallel after T019-T020 define the expected behavior.
- **US2**: Run T031, T033, and T037 in parallel after T029-T030.
- **US9**: Run T041, T043, and T044 in parallel after T039-T040.
- **US3**: Run T051, T053, and T057 in parallel after T049-T050.
- **US4**: Run T061, T063, and T067 in parallel after T059-T060.
- **US10**: Run T070 and T071 in parallel after T068-T069.
- **US5**: Run T077, T079, and T084 in parallel after T074-T076.
- **US6**: Run T088, T090, and T094 in parallel after T086-T087.
- **US7**: Run T097, T099, and T101 in parallel after T095-T096.
- **US8**: Run T108, T109, and T110 in parallel after T104-T107.
- **US5 completion**: Include T121 and T122 before marking checkout side effects done.

---

## Implementation Strategy

### Suggested MVP Scope

1. Complete Phase 1 and Phase 2.
2. Deliver US1, US2, and US9 as the first deployable slice.
3. Validate registration, catalog browsing, and gateway routing before starting cart/checkout work.

### Incremental Delivery

1. **Foundation**: Setup + Foundational.
2. **MVP**: US1 + US2 + US9.
3. **Commerce**: US3 + US4 + US10 + US5.
4. **Retention**: US6 + US7.
5. **Operations**: US8 + Polish.

### Execution Notes

- Write the story tests before implementation and confirm they fail for the expected reason.
- Complete T118 before starting story implementation so API-first requirements remain constitution-compliant.
- Keep domain code free of Django imports.
- Prefer one logical commit per completed task or small task bundle.
- Stop at each checkpoint and validate the story independently before continuing.
