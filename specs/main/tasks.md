---
description: "Task list for Mango Microservices E-Commerce Platform"
---

# Tasks: Mango Microservices E-Commerce Platform

**Input**: Design documents from `/specs/001-mango-ecommerce-platform/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

- [X] T001 Create project structure per implementation plan (services/, shared/, frontend/, specs/)
- [X] T002 Initialize Python/Django projects for each microservice in services/
- [X] T003 Initialize Next.js project in frontend/
- [X] T004 [P] Add Poetry and pnpm config files to root and services/frontend
- [X] T005 [P] Add Dockerfiles and docker-compose.yml for all services
- [X] T006 [P] Add .env.example files for all services and frontend
- [X] T007 [P] Configure pre-commit, linting, and formatting tools (black, isort, flake8, prettier)

---

## Phase 2: Foundational (Blocking Prerequisites)

- [X] T008 Setup shared message bus library in shared/message_bus/
- [X] T009 [P] Implement base domain entities and value objects in each service (domain/entities.py)
- [X] T010 [P] Setup database schema and migrations for all services
- [X] T011 [P] Implement base JWT authentication and middleware in auth_service and gateway
- [X] T012 [P] Implement API Gateway routing, rate limiting, and error normalization in gateway/
- [X] T013 [P] Setup CI pipeline for lint, test, build, and deploy
- [X] T014 Configure logging, observability, and health checks for all services
- [X] T015 Setup environment configuration management for all services
- [ ] T012 [P] Implement API Gateway routing, rate limiting, and error normalization in gateway/
- [ ] T013 [P] Setup CI pipeline for lint, test, build, and deploy
- [ ] T014 Configure logging, observability, and health checks for all services
- [ ] T015 Setup environment configuration management for all services

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Allow users to register, log in, receive confirmation email, and manage sessions. Admins can log in with elevated privileges.

**Independent Test**: Register a new user, log in, verify session token, and admin login.

- [X] T016 [P] [US1] Create User and RefreshToken models in services/auth_service/domain/entities.py
- [X] T017 [P] [US1] Implement UserRepository and token logic in services/auth_service/infrastructure/repositories.py
- [X] T018 [P] [US1] Implement registration, login, password reset, and admin login endpoints in services/auth_service/presentation/views.py
- [X] T019 [US1] Implement JWT issuance and session management in services/auth_service/application/use_cases/
- [X] T020 [US1] Integrate email event publishing for registration and password reset
- [X] T021 [US1] Add account lockout logic after failed attempts
- [X] T022 [US1] Add role-based access control (Customer/Admin)
- [X] T023 [US1] Add contract and integration tests for registration, login, and password reset in services/auth_service/tests/

---

## Phase 4: User Story 2 - Browse and Search Product Catalog (Priority: P1)

**Goal**: Allow users to browse, filter, and search products, and view product details.

**Independent Test**: Load catalog, filter by category, search, and view product detail page.

- [ ] T024 [P] [US2] Create Category and Product models in services/product_service/domain/entities.py
- [ ] T025 [P] [US2] Implement ProductRepository and CategoryRepository in services/product_service/infrastructure/repositories.py
- [ ] T026 [P] [US2] Implement product listing, filtering, search, and detail endpoints in services/product_service/presentation/views.py
- [ ] T027 [US2] Add pagination, sorting, and out-of-stock logic
- [ ] T028 [US2] Add contract and integration tests for catalog and product detail in services/product_service/tests/

---

## Phase 5: User Story 3 - Shopping Cart Management (Priority: P2)

**Goal**: Allow users to add, update, and remove items in their cart, with persistence across sessions.

**Independent Test**: Add products to cart, update quantities, remove items, log out/in, verify cart state.

- [ ] T029 [P] [US3] Create Cart and CartItem models in services/cart_service/domain/entities.py
- [ ] T030 [P] [US3] Implement CartRepository in services/cart_service/infrastructure/repositories.py
- [ ] T031 [P] [US3] Implement add, update, remove, and view cart endpoints in services/cart_service/presentation/views.py
- [ ] T032 [US3] Implement cart persistence and subtotal calculation
- [ ] T033 [US3] Add contract and integration tests for cart operations in services/cart_service/tests/

---

## Phase 6: User Story 4 - Apply Coupons and Discounts (Priority: P2)

**Goal**: Allow users to apply coupons at checkout, validate, and reflect discounts.

**Independent Test**: Create coupon, add items to cart, apply coupon, verify discount.

- [ ] T034 [P] [US4] Create Coupon and CouponUsage models in services/coupon_service/domain/entities.py
- [ ] T035 [P] [US4] Implement CouponRepository in services/coupon_service/infrastructure/repositories.py
- [ ] T036 [P] [US4] Implement coupon validation and redemption endpoints in services/coupon_service/presentation/views.py
- [ ] T037 [US4] Integrate coupon validation with cart and order services
- [ ] T038 [US4] Add contract and integration tests for coupon flows in services/coupon_service/tests/

---

## Phase 7: User Story 5 - Place an Order and Process Payment (Priority: P2)

**Goal**: Allow users to checkout, provide shipping, process payment, and confirm order.

**Independent Test**: Complete purchase flow, verify order in history, and inventory update.

- [ ] T039 [P] [US5] Create Order and OrderItem models in services/order_service/domain/entities.py
- [ ] T040 [P] [US5] Implement OrderRepository in services/order_service/infrastructure/repositories.py
- [ ] T041 [P] [US5] Implement order creation, payment, and history endpoints in services/order_service/presentation/views.py
- [ ] T042 [US5] Integrate with payment provider and inventory update
- [ ] T043 [US5] Add contract and integration tests for order flows in services/order_service/tests/

---

## Phase 8: User Story 6 - Reward Points Program (Priority: P3)

**Goal**: Credit and redeem reward points, view balance and history, enforce redemption rules.

**Independent Test**: Make purchase, verify points credited, redeem points, and view dashboard.

- [ ] T044 [P] [US6] Create RewardAccount and RewardTransaction models in services/reward_service/domain/entities.py
- [ ] T045 [P] [US6] Implement RewardRepository in services/reward_service/infrastructure/repositories.py
- [ ] T046 [P] [US6] Implement reward credit, redemption, and history endpoints in services/reward_service/presentation/views.py
- [ ] T047 [US6] Integrate reward logic with order and coupon services
- [ ] T048 [US6] Add contract and integration tests for rewards in services/reward_service/tests/

---

## Phase 9: User Story 7 - Transactional Email Notifications (Priority: P3)

**Goal**: Send emails for registration, password reset, order confirmation, status updates, and rewards.

**Independent Test**: Trigger events and verify emails are queued and delivered.

- [ ] T049 [P] [US7] Create EmailMessage model in services/email_service/domain/entities.py
- [ ] T050 [P] [US7] Implement EmailRepository in services/email_service/infrastructure/repositories.py
- [ ] T051 [P] [US7] Implement event consumers and email sending logic in services/email_service/application/use_cases/
- [ ] T052 [US7] Add contract and integration tests for email events in services/email_service/tests/

---

## Phase 10: User Story 8 - Admin Product Management (Priority: P3)

**Goal**: Admins can create, update, delete products, manage categories, prices, images, and inventory.

**Independent Test**: Admin creates/updates/deletes product, changes reflected on storefront.

- [ ] T053 [P] [US8] Implement admin endpoints for product/category CRUD in services/product_service/presentation/views.py
- [ ] T054 [US8] Add admin contract and integration tests in services/product_service/tests/

---

## Phase 11: User Story 9 - API Gateway Routing and Cross-Cutting Concerns (Priority: P1)

**Goal**: Route all frontend requests through gateway, handle auth, rate limiting, and logging.

**Independent Test**: Requests routed, tokens validated, rate limits enforced, errors handled.

- [ ] T055 [P] [US9] Implement gateway route map and service proxying in services/gateway/
- [ ] T056 [P] [US9] Implement authentication, rate limiting, and error handling middleware in services/gateway/
- [ ] T057 [US9] Add contract and integration tests for gateway routing in services/gateway/tests/

---

## Phase 12: User Story 10 - Asynchronous Inter-Service Messaging (Priority: P2)

**Goal**: Publish and consume domain events for order, email, reward, and inventory updates.

**Independent Test**: Place order, verify events published and consumed, and side effects processed.

- [ ] T058 [P] [US10] Implement message bus event publishing in all services (shared/message_bus/)
- [ ] T059 [P] [US10] Implement event consumers for order, email, reward, and product services
- [ ] T060 [US10] Add contract and integration tests for event flows in shared/testing/

---



## Phase 13: Polish & Cross-Cutting Concerns

- [ ] T061 [P] Documentation and quickstart validation: Update all specs/, docs/, and validate quickstart.md. Acceptance: All documentation up to date and quickstart passes end-to-end setup test.
- [ ] T062 Code cleanup and refactoring across all services
- [ ] T063 Performance optimization and load testing: Profile all services, optimize slowest endpoints, and run load tests. Acceptance: 95th percentile response time <2s under 1,000 RPS sustained load; bottlenecks documented and addressed.
- [ ] T064 [P] Additional unit tests in all services/tests/unit/
- [ ] T065 Security hardening and audit: Conduct penetration testing, static analysis, and dependency vulnerability scans. Acceptance: All critical/high vulnerabilities remediated; security audit report completed and signed off.

- [ ] T067 Scalability testing: Simulate high concurrent users and measure system throughput. Acceptance: System supports 10,000+ concurrent users with <2s response time for 95% of requests.
- [ ] T068 Compliance audit: Review and document GDPR, PCI-DSS, and local regulatory requirements. Acceptance: Compliance checklist completed and signed off.
- [ ] T069 Accessibility validation: Run WCAG 2.1 AA audits on frontend. Acceptance: All critical user flows pass accessibility checks.
- [ ] T070 Reliability/Resilience: Perform chaos testing and failover drills. Acceptance: No data loss and <1 min recovery from simulated failures.
- [ ] T071 Maintainability: Review codebase for modularity, documentation, and adherence to Clean Architecture. Acceptance: 100% of modules pass maintainability checklist.
- [ ] T072 Availability: Set up uptime monitoring and alerting. Acceptance: 99.9% uptime over 30-day rolling window.
- [ ] T073 Data privacy: Validate data encryption at rest and in transit. Acceptance: All sensitive fields encrypted and verified in test.

# Non-Functional Requirements (Explicit, Testable Tasks)
- [ ] T067 Scalability testing: Simulate high concurrent users and measure system throughput. Acceptance: System supports 10,000+ concurrent users with <2s response time for 95% of requests.
- [ ] T068 Compliance audit: Review and document GDPR, PCI-DSS, and local regulatory requirements. Acceptance: Compliance checklist completed and signed off.
- [ ] T069 Accessibility validation: Run WCAG 2.1 AA audits on frontend. Acceptance: All critical user flows pass accessibility checks.
- [ ] T070 Reliability/Resilience: Perform chaos testing and failover drills. Acceptance: No data loss and <1 min recovery from simulated failures.
- [ ] T071 Maintainability: Review codebase for modularity, documentation, and adherence to Clean Architecture. Acceptance: 100% of modules pass maintainability checklist.
- [ ] T072 Availability: Set up uptime monitoring and alerting. Acceptance: 99.9% uptime over 30-day rolling window.
- [ ] T073 Data privacy: Validate data encryption at rest and in transit. Acceptance: All sensitive fields encrypted and verified in test.

---

## Dependencies & Execution Order

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Depends on US1 (auth) and US2 (products)
- **User Story 4 (P2)**: Depends on US3 (cart)
- **User Story 5 (P2)**: Depends on US3 (cart), US4 (coupon), US6 (reward)
- **User Story 6 (P3)**: Depends on US5 (order)
- **User Story 7 (P3)**: Depends on US1 (auth), US5 (order), US6 (reward)
- **User Story 8 (P3)**: Depends on US1 (admin auth), US2 (products)
- **User Story 9 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 10 (P2)**: Depends on US5 (order), US7 (email), US6 (reward)

### Parallel Execution Examples

- All [P] tasks in Setup and Foundational can run in parallel
- All user stories can be developed in parallel after Foundational phase
- Within each user story, [P] tasks (models, repositories, endpoints) can run in parallel
- Tests for each user story can be written in parallel

---

## Implementation Strategy

- **MVP First**: Complete Setup, Foundational, and User Story 1 (auth) for a working identity backbone
- **Incremental Delivery**: Add each user story in priority order, test independently, and deploy
- **Parallel Team**: Assign user stories to different team members after Foundational phase

---
