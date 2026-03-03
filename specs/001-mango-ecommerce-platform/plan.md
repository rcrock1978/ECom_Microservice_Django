# Implementation Plan: Mango Microservices E-Commerce Platform

**Branch**: `001-mango-ecommerce-platform` | **Date**: 2026-03-04 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-mango-ecommerce-platform/spec.md`

## Summary

Build a full-stack e-commerce platform using Python Django REST Framework microservices with a Next.js frontend. The system comprises 7 domain microservices (Auth, Product, Cart, Order, Coupon, Reward, Email), a custom Django API Gateway, and a shared message bus library using Celery + RabbitMQ. Clean Architecture patterns are enforced in each service with strict layer separation. Event-driven communication decouples services while PostgreSQL provides per-service data persistence and Redis handles caching/sessions.

## Technical Context

**Language/Version**: Python 3.12, TypeScript 5.x (Node.js 20+)
**Primary Dependencies**: Django 5.x, Django REST Framework, Celery 5.x, Next.js 14+ (App Router), httpx, djangorestframework-simplejwt
**Storage**: PostgreSQL 16 (separate schema per service in dev, separate instances in prod), Redis 7+ (cache/sessions)
**Testing**: pytest + pytest-django + factory_boy + httpx (backend), Jest + React Testing Library (frontend)
**Target Platform**: Linux containers (Docker/Kubernetes)
**Project Type**: web-service (microservices + SPA frontend)
**Performance Goals**: 1000 concurrent users, <2s search response, <1s coupon validation, <60s email delivery
**Constraints**: <200ms p95 API response time, at-least-once message delivery, zero shared databases between services
**Scale/Scope**: 7 microservices + 1 gateway + 1 frontend, 11 database tables, 8 event types, ~15 screens

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Clean Architecture | PASS | Each service uses Domain/Application/Infrastructure/Presentation layers. Domain entities are plain Python dataclasses with zero Django imports. |
| II. Service Autonomy | PASS | Each service has its own DB schema, Dockerfile, and deployment unit. Communication only via API contracts or message bus events. |
| III. Test-First Development | PASS | pytest suite per service with unit/integration/contract test structure. 80% coverage target. |
| IV. Event-Driven Communication | PASS | Celery + RabbitMQ with topic exchanges, at-least-once delivery, idempotent consumers, dead-letter queues. |
| V. API-First Design | PASS | All contracts defined in contracts/ directory before implementation. Gateway is single frontend entry point. Consistent error format. |
| VI. Observability and Logging | PASS | Structured JSON logging, correlation IDs via X-Request-ID header, health check endpoints on all services. |
| VII. Simplicity and YAGNI | PASS | Custom Django gateway over Kong (simpler, same stack). Single monorepo over polyrepo. Shared Celery over raw pika. |

**Gate Result: ALL PASS** - No violations. Proceed to implementation.

## Project Structure

### Documentation (this feature)

```
specs/001-mango-ecommerce-platform/
+-- plan.md              # This file
+-- research.md          # Phase 0: Technology decisions
+-- data-model.md        # Phase 1: Entity definitions per service
+-- quickstart.md        # Phase 1: Getting started guide
+-- contracts/           # Phase 1: API and event contracts
|   +-- gateway-routes.md
|   +-- auth-api.md
|   +-- product-api.md
|   +-- cart-api.md
|   +-- order-api.md
|   +-- coupon-api.md
|   +-- reward-api.md
|   +-- email-api.md
|   +-- message-bus-events.md
+-- checklists/
|   +-- requirements.md
+-- tasks.md             # Phase 2: Implementation tasks (created by /speckit.tasks)
```

### Source Code (repository root)

```
ecom_microservices/
+-- services/                        # All Django microservices
|   +-- gateway/                     # Mango.GatewaySolution
|   |   +-- gateway/
|   |   |   +-- domain/              # Route config, rate limit rules
|   |   |   +-- application/         # Proxy use cases
|   |   |   +-- infrastructure/      # httpx client, JWT validation
|   |   |   +-- presentation/        # Django views, middleware
|   |   +-- tests/
|   |   +-- manage.py
|   |   +-- pyproject.toml
|   |   +-- Dockerfile
|   +-- auth_service/                # Mango.Services.AuthAPI
|   |   +-- auth/
|   |   |   +-- domain/              # User entity, value objects
|   |   |   +-- application/         # Register, Login, ResetPassword use cases
|   |   |   +-- infrastructure/      # Django ORM models, JWT provider
|   |   |   +-- presentation/        # DRF serializers, views, urls
|   |   +-- tests/
|   |   +-- manage.py
|   |   +-- pyproject.toml
|   |   +-- Dockerfile
|   +-- product_service/             # Mango.Services.ProductAPI
|   |   +-- catalog/
|   |   |   +-- domain/
|   |   |   +-- application/
|   |   |   +-- infrastructure/
|   |   |   +-- presentation/
|   |   +-- tests/
|   |   +-- manage.py
|   |   +-- pyproject.toml
|   |   +-- Dockerfile
|   +-- cart_service/                # Mango.Services.ShoppingCartAPI
|   |   +-- cart/
|   |   |   +-- domain/
|   |   |   +-- application/
|   |   |   +-- infrastructure/
|   |   |   +-- presentation/
|   |   +-- tests/
|   |   +-- manage.py
|   |   +-- pyproject.toml
|   |   +-- Dockerfile
|   +-- order_service/               # Mango.Services.OrderAPI
|   |   +-- orders/
|   |   |   +-- domain/
|   |   |   +-- application/
|   |   |   +-- infrastructure/
|   |   |   +-- presentation/
|   |   +-- tests/
|   |   +-- manage.py
|   |   +-- pyproject.toml
|   |   +-- Dockerfile
|   +-- coupon_service/              # Mango.Services.CouponAPI
|   |   +-- coupons/
|   |   |   +-- domain/
|   |   |   +-- application/
|   |   |   +-- infrastructure/
|   |   |   +-- presentation/
|   |   +-- tests/
|   |   +-- manage.py
|   |   +-- pyproject.toml
|   |   +-- Dockerfile
|   +-- reward_service/              # Mango.Services.RewardAPI
|   |   +-- rewards/
|   |   |   +-- domain/
|   |   |   +-- application/
|   |   |   +-- infrastructure/
|   |   |   +-- presentation/
|   |   +-- tests/
|   |   +-- manage.py
|   |   +-- pyproject.toml
|   |   +-- Dockerfile
|   +-- email_service/               # Mango.Services.EmailAPI
|   |   +-- emails/
|   |   |   +-- domain/
|   |   |   +-- application/
|   |   |   +-- infrastructure/
|   |   |   +-- presentation/
|   |   +-- tests/
|   |   +-- manage.py
|   |   +-- pyproject.toml
|   |   +-- Dockerfile
+-- shared/                          # Mango.MessageBus (shared library)
|   +-- message_bus/                 # Event publishing/consuming base
|   |   +-- events.py               # Event envelope, base event class
|   |   +-- publisher.py            # Celery task publisher
|   |   +-- consumer.py             # Base consumer with idempotency
|   +-- common/                     # Shared utilities
|   |   +-- exceptions.py           # Standard error types
|   |   +-- responses.py            # Consistent response format
|   |   +-- middleware.py           # Correlation ID, logging
|   +-- testing/                    # Shared test utilities
|   |   +-- factories.py
|   |   +-- fixtures.py
|   +-- pyproject.toml
+-- frontend/                        # Mango.Web (Next.js 14+)
|   +-- src/
|   |   +-- app/                    # App Router pages
|   |   |   +-- (auth)/             # Login, register, forgot password
|   |   |   +-- products/           # Catalog, product detail
|   |   |   +-- cart/               # Cart page
|   |   |   +-- checkout/           # Checkout flow
|   |   |   +-- orders/             # Order history, detail
|   |   |   +-- rewards/            # Rewards dashboard
|   |   |   +-- admin/              # Admin pages
|   |   +-- components/             # Reusable React components
|   |   |   +-- ui/                 # Design system primitives
|   |   |   +-- products/           # Product card, grid, detail
|   |   |   +-- cart/               # Cart drawer, item row
|   |   |   +-- layout/             # Header, footer, nav
|   |   +-- lib/                    # API client, utilities
|   |   |   +-- api/                # Gateway API client (fetch wrapper)
|   |   |   +-- auth/               # Auth context, token handling
|   |   |   +-- cart/               # Cart context provider
|   |   +-- types/                  # TypeScript type definitions
|   +-- tests/
|   +-- package.json
|   +-- pnpm-lock.yaml
|   +-- next.config.js
|   +-- Dockerfile
+-- docker-compose.yml               # Development orchestration
+-- docker-compose.prod.yml          # Production overrides
+-- .env.example                     # Environment variable template
+-- specs/                           # Feature specifications
+-- .specify/                        # SpecKit configuration
```

**Structure Decision**: Monorepo with `services/` directory containing one Django project per microservice, a `shared/` library for message bus and common utilities (installed as editable dependency), and a `frontend/` Next.js application. Each service follows identical internal structure with Clean Architecture layers (domain/application/infrastructure/presentation). This mirrors the original Mango Microservices naming (Mango.Services.AuthAPI etc.) while following Python/Django conventions.

## Complexity Tracking

No constitution violations to justify. All complexity decisions align with the constitution:

| Decision | Justification | Simpler Alternative Rejected Because |
|----------|--------------|-------------------------------------|
| 9 deployable units (7 services + gateway + frontend) | Required by spec (each service independently deployable per FR-045) | Monolith rejected — contradicts Service Autonomy principle |
| Shared library (`shared/`) | Avoid duplicating message bus, error format, middleware across 7 services | Copy-paste rejected — violates DRY, makes contract changes error-prone |
| Custom Django gateway over Kong | Same tech stack, zero learning curve, <500 lines of code | Kong rejected — separate technology (Lua/Go), requires own database, overkill for 7 services |
| Celery over raw pika | Built-in retries, DLQ, monitoring (Flower), first-class Django integration | Raw pika rejected — requires manual retry logic, connection management, no monitoring |
