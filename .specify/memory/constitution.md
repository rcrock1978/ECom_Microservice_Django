# Mango Microservices E-Commerce Platform Constitution

## Core Principles

### I. Clean Architecture (NON-NEGOTIABLE)
Each microservice follows Clean Architecture with strict layer separation: Domain (entities, value objects) -> Application (use cases, interfaces) -> Infrastructure (Django ORM, external APIs) -> Presentation (DRF serializers, views). Dependencies point inward only. Domain layer has ZERO framework imports.

### II. Service Autonomy
Each microservice owns its data, schema, and deployment lifecycle. No shared databases between services. Services communicate only via published API contracts or message bus events. Each service is independently deployable, testable, and scalable.

### III. Test-First Development (NON-NEGOTIABLE)
TDD mandatory: Write tests first -> Verify they fail -> Implement -> Verify they pass -> Refactor. Unit tests for domain logic, integration tests for API contracts, contract tests for inter-service communication. Minimum 80% code coverage per service.

### IV. Event-Driven Communication
Services communicate asynchronously via message bus for state changes. Synchronous HTTP only for queries and direct user-facing requests. Events are published with at-least-once delivery semantics. Consumers must be idempotent. Dead-letter queues for failed messages.

### V. API-First Design
All service interfaces defined as OpenAPI contracts before implementation. Frontend consumes only the API Gateway; never calls services directly. Versioned APIs with backward compatibility guarantees. Consistent error response format across all services.

### VI. Observability and Logging
Structured JSON logging in every service. Correlation IDs propagated across service boundaries. Health check endpoints on every service. Request/response logging at gateway level. Performance metrics for all critical paths.

### VII. Simplicity and YAGNI
Start with the simplest solution that meets requirements. No premature optimization. No speculative features. Complexity must be justified against a simpler rejected alternative. Prefer convention over configuration.

## Technology Stack

- **Backend Framework**: Python 3.12 + Django 5.x + Django REST Framework
- **Frontend Framework**: Next.js 14+ (App Router) with TypeScript
- **Database**: PostgreSQL 16 (one instance per service in production; shared instance with separate schemas acceptable in dev)
- **Message Broker**: RabbitMQ 3.13+ with topic exchanges
- **API Gateway**: Custom Django gateway service (chosen over Kong for same-stack simplicity)
- **Cache**: Redis 7+ for session storage, rate limiting, and cart caching
- **Task Queue**: Celery 5.x with RabbitMQ backend (for async email, reward processing)
- **Authentication**: JWT (access + refresh tokens) via djangorestframework-simplejwt
- **Object Storage**: S3-compatible (MinIO for local dev, AWS S3 for production)
- **Containerization**: Docker with Docker Compose (dev), Kubernetes (production)
- **Testing**: pytest + pytest-django + factory_boy + httpx (contract tests)
- **Package Management**: Poetry (Python), pnpm (Node.js/Next.js)

## Development Workflow

- Feature branches from main with naming convention NNN-feature-name
- All changes require passing CI pipeline: lint -> unit tests -> integration tests -> build
- Code review required before merge to main
- Database migrations are forward-only; no destructive migrations without migration plan
- Environment configuration via environment variables (python-decouple or django-environ)
- Local development via Docker Compose with all services, database, RabbitMQ, and Redis

## Governance

This constitution supersedes all other development practices for this project. Amendments require documentation of the change, rationale, and migration plan for existing code. All PRs must verify compliance with these principles. Violations must be justified in the Complexity Tracking section of the implementation plan.

**Version**: 1.0.0 | **Ratified**: 2026-03-04 | **Last Amended**: 2026-03-04
