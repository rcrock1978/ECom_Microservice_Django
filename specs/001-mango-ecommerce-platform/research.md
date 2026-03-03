# Technology Research: Mango Microservices E-Commerce Platform

**Created**: 2026-03-04  
**Feature**: 001-mango-ecommerce-platform  
**Purpose**: Detailed technology decisions with rationale for all major architectural choices

---

## 1. API Gateway Choice

### Decision: Custom Django Gateway Service

Use a **lightweight custom Django gateway service** built with Django REST Framework + `httpx` (async HTTP client) for request proxying, combined with middleware for JWT validation and rate limiting.

### Rationale

| Factor | Kong | Custom Django Gateway | Traefik/NGINX |
|--------|------|----------------------|---------------|
| **Setup complexity** | High — requires separate Lua/Go runtime, declarative config, its own PostgreSQL database | Low — same stack as all other services (Python/Django/DRF) | Medium — config-file based, reverse proxy only |
| **JWT validation** | Built-in plugin, but configuration is YAML/Admin API | Native via `djangorestframework-simplejwt` — same library as Auth service | Requires external auth service or Lua/OpenResty plugin |
| **Rate limiting** | Built-in plugin (Redis-backed) | `django-ratelimit` or `djangorestframework-throttling` — 20 lines of code | Basic rate limiting via modules; advanced requires Lua |
| **Service discovery** | Built-in DNS/Consul integration | Docker Compose DNS (`http://product-service:8000`) — sufficient for dev; Kubernetes DNS for prod | Docker labels or static config |
| **Team knowledge** | Requires learning Kong's config model | Zero learning curve — team already knows Django | Configuration language, not code |
| **Debugging** | Opaque proxy; separate logging | Full Python debugging, same logging as all services | Access logs only |
| **Custom logic** | Lua plugins or Go plugins | Native Python — correlation IDs, request transformation, response aggregation trivially added | Very limited custom logic |
| **Resource overhead** | ~200MB+ additional container (Kong + its DB) | ~80MB (same as any Django service) | ~20MB (lightweight) |

**Why not Kong?** Kong is excellent for large organizations with dedicated platform teams. For a 7-service platform built entirely in Django, it introduces an entirely separate technology (Lua/Go), requires its own database, and adds operational complexity disproportionate to the benefits. Every capability Kong provides (JWT validation, rate limiting, routing, logging) can be implemented in <500 lines of Django code, using libraries the team already knows.

**Why not Traefik/NGINX?** These are reverse proxies, not application gateways. They route requests but cannot perform application-level logic like: enriching requests with user context from JWT claims, aggregating responses from multiple services, applying business-level rate limiting rules, or transforming error responses into a consistent format. You'd end up needing a custom service behind them anyway.

**Custom gateway architecture:**

```
┌─────────────┐     ┌──────────────────────────────────┐     ┌─────────────────┐
│   Next.js   │────▶│     Django Gateway Service        │────▶│  Auth Service    │
│  Frontend   │     │                                    │────▶│  Product Service │
│             │◀────│  • JWT middleware (simplejwt)       │────▶│  Cart Service    │
│             │     │  • Rate limit middleware            │────▶│  Order Service   │
│             │     │  • Correlation ID middleware        │────▶│  Coupon Service  │
│             │     │  • Route config (URL → service map) │────▶│  Reward Service  │
│             │     │  • httpx async proxy                │────▶│  Email Service   │
│             │     │  • Error normalization              │     │                 │
└─────────────┘     └──────────────────────────────────┘     └─────────────────┘
```

```python
# Example: gateway/routing.py — simplified route configuration
SERVICE_ROUTES = {
    "/api/auth/":     {"upstream": "http://auth-service:8000",     "auth_required": False},
    "/api/products/": {"upstream": "http://product-service:8000",  "auth_required": False},
    "/api/cart/":     {"upstream": "http://cart-service:8000",     "auth_required": True},
    "/api/orders/":   {"upstream": "http://order-service:8000",    "auth_required": True},
    "/api/coupons/":  {"upstream": "http://coupon-service:8000",   "auth_required": True},
    "/api/rewards/":  {"upstream": "http://reward-service:8000",   "auth_required": True},
}
```

```python
# Example: gateway/middleware.py — JWT validation middleware
import httpx
from rest_framework_simplejwt.tokens import AccessToken

class GatewayJWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        route_config = match_route(request.path)
        if route_config and route_config["auth_required"]:
            token = extract_bearer_token(request)
            if not token:
                return JsonResponse({"error": "Authentication required"}, status=401)
            try:
                validated = AccessToken(token)
                # Inject user context as headers for downstream services
                request.META["HTTP_X_USER_ID"] = str(validated["user_id"])
                request.META["HTTP_X_USER_ROLE"] = validated.get("role", "customer")
            except Exception:
                return JsonResponse({"error": "Invalid or expired token"}, status=401)
        return self.get_response(request)
```

```python
# Example: gateway/views.py — async proxy view
import httpx
from django.http import StreamingHttpResponse

async def proxy_request(request, upstream_url):
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.request(
            method=request.method,
            url=upstream_url,
            headers=forward_headers(request),
            content=request.body,
        )
        return StreamingHttpResponse(
            response.iter_bytes(),
            status=response.status_code,
            content_type=response.headers.get("content-type"),
        )
```

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| **Kong Gateway** | Operational overhead (separate DB, Lua plugins, Admin API) disproportionate for 7-service platform. Team has no Lua/Go expertise. |
| **Traefik** | Reverse proxy only — cannot perform JWT claim extraction, response aggregation, or business-level request transformation. |
| **NGINX + Lua (OpenResty)** | Similar power to Kong but even more Lua exposure. Niche skill set. |
| **FastAPI Gateway** | Would work technically (better async story), but introduces a second Python framework. Constitution says Django/DRF for backend. |
| **AWS API Gateway / GCP Endpoints** | Cloud-vendor lock-in. Doesn't work in local Docker Compose development. |

---

## 2. Clean Architecture in Django

### Decision: Layered Package Structure per Django App

Each microservice is a standalone Django project containing a single Django app (or a small number of apps) with explicit **domain**, **application**, **infrastructure**, and **presentation** packages. The domain layer uses **plain Python classes only** (zero Django imports).

### Rationale

Django's default structure (`models.py`, `views.py`, `serializers.py`) conflates all layers into a flat namespace. Clean Architecture requires explicit boundaries. The key insight: **Django ORM models live in the infrastructure layer, not the domain layer**. Domain entities are plain Python dataclasses or Pydantic models. Infrastructure "repository" classes translate between domain entities and Django ORM models.

**Folder structure for each microservice:**

```
order_service/                      # Django project root
├── manage.py
├── config/                         # Django project settings
│   ├── __init__.py
│   ├── settings.py                 # (or settings/ with base, dev, prod)
│   ├── urls.py                     # Root URL config — delegates to presentation
│   ├── asgi.py
│   └── wsgi.py
│
├── order/                          # The main Django app
│   ├── __init__.py
│   │
│   ├── domain/                     # ① DOMAIN LAYER — pure Python, ZERO Django imports
│   │   ├── __init__.py
│   │   ├── entities.py             # Domain entities (dataclasses/attrs)
│   │   ├── value_objects.py        # Value objects (Money, Address, OrderStatus)
│   │   ├── exceptions.py           # Domain-specific exceptions
│   │   ├── events.py               # Domain events (OrderConfirmed, OrderCancelled)
│   │   └── interfaces.py           # Abstract repository interfaces (ABCs)
│   │
│   ├── application/                # ② APPLICATION LAYER — use cases, orchestration
│   │   ├── __init__.py
│   │   ├── use_cases/              # One file per use case
│   │   │   ├── __init__.py
│   │   │   ├── create_order.py     # CreateOrderUseCase
│   │   │   ├── cancel_order.py     # CancelOrderUseCase
│   │   │   └── get_order_history.py
│   │   ├── dto.py                  # Data Transfer Objects (input/output)
│   │   └── interfaces.py           # Application-level interfaces (e.g., PaymentGateway, EventPublisher)
│   │
│   ├── infrastructure/             # ③ INFRASTRUCTURE LAYER — Django ORM, external APIs
│   │   ├── __init__.py
│   │   ├── models.py               # Django ORM models (registered with Django)
│   │   ├── repositories.py         # Concrete implementations of domain interfaces
│   │   ├── event_publisher.py      # RabbitMQ publisher implementation
│   │   ├── payment_gateway.py      # Stripe client implementation
│   │   ├── admin.py                # Django admin (optional)
│   │   └── migrations/             # Django migrations
│   │       └── __init__.py
│   │
│   └── presentation/               # ④ PRESENTATION LAYER — DRF views, serializers, URLs
│       ├── __init__.py
│       ├── serializers.py          # DRF serializers (input validation, output formatting)
│       ├── views.py                # DRF ViewSets or APIViews
│       ├── urls.py                 # URL routing for this app
│       └── permissions.py          # DRF permission classes
│
├── tests/                          # Test directory mirrors the layers
│   ├── __init__.py
│   ├── unit/                       # Domain + Application tests (no DB needed)
│   │   ├── __init__.py
│   │   ├── test_entities.py
│   │   ├── test_value_objects.py
│   │   └── test_use_cases.py
│   ├── integration/                # Infrastructure tests (DB, RabbitMQ)
│   │   ├── __init__.py
│   │   ├── test_repositories.py
│   │   └── test_event_publisher.py
│   └── contract/                   # API contract tests
│       ├── __init__.py
│       └── test_api.py
│
├── pyproject.toml                  # Poetry config
├── Dockerfile
└── docker-compose.yml              # Per-service compose (overrides base)
```

**Key implementation patterns:**

```python
# ① domain/entities.py — PURE PYTHON, no Django imports
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

@dataclass
class OrderItem:
    product_id: UUID          # Reference to Product service's product (ID only)
    product_name: str         # Denormalized at order creation time
    quantity: int
    unit_price: Decimal

    @property
    def line_total(self) -> Decimal:
        return self.unit_price * self.quantity

@dataclass
class Order:
    id: UUID = field(default_factory=uuid4)
    customer_id: UUID = field(default=None)
    items: list[OrderItem] = field(default_factory=list)
    status: OrderStatus = field(default=OrderStatus.PENDING)
    coupon_discount: Decimal = field(default=Decimal("0.00"))
    reward_points_discount: Decimal = field(default=Decimal("0.00"))
    created_at: datetime = field(default=None)

    @property
    def subtotal(self) -> Decimal:
        return sum(item.line_total for item in self.items)

    @property
    def total(self) -> Decimal:
        return max(self.subtotal - self.coupon_discount - self.reward_points_discount, Decimal("0.00"))

    def confirm(self) -> "OrderConfirmedEvent":
        if self.status != OrderStatus.PENDING:
            raise DomainException(f"Cannot confirm order in {self.status} status")
        self.status = OrderStatus.CONFIRMED
        return OrderConfirmedEvent(order_id=self.id, customer_id=self.customer_id, total=self.total)
```

```python
# ① domain/interfaces.py — abstract contracts (no Django)
from abc import ABC, abstractmethod
from uuid import UUID

class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> Order: ...

    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Order | None: ...

    @abstractmethod
    def list_by_customer(self, customer_id: UUID) -> list[Order]: ...

class EventPublisher(ABC):
    @abstractmethod
    def publish(self, event: DomainEvent) -> None: ...
```

```python
# ② application/use_cases/create_order.py — orchestrates domain + infrastructure
from order.domain.entities import Order, OrderItem
from order.domain.interfaces import OrderRepository, EventPublisher

class CreateOrderUseCase:
    def __init__(self, order_repo: OrderRepository, event_publisher: EventPublisher):
        self.order_repo = order_repo
        self.event_publisher = event_publisher

    def execute(self, input_dto: CreateOrderInput) -> CreateOrderOutput:
        order = Order(
            customer_id=input_dto.customer_id,
            items=[OrderItem(**item) for item in input_dto.items],
        )
        event = order.confirm()
        saved_order = self.order_repo.save(order)
        self.event_publisher.publish(event)
        return CreateOrderOutput(order_id=saved_order.id, status=saved_order.status.value)
```

```python
# ③ infrastructure/repositories.py — Django ORM implementation
from order.domain.entities import Order as OrderEntity
from order.domain.interfaces import OrderRepository
from order.infrastructure.models import OrderModel, OrderItemModel

class DjangoOrderRepository(OrderRepository):
    def save(self, order: OrderEntity) -> OrderEntity:
        db_order, _ = OrderModel.objects.update_or_create(
            id=order.id,
            defaults={
                "customer_id": order.customer_id,
                "status": order.status.value,
                "coupon_discount": order.coupon_discount,
            },
        )
        # Save items...
        return self._to_entity(db_order)

    def _to_entity(self, db_order: OrderModel) -> OrderEntity:
        """Map ORM model → domain entity"""
        return OrderEntity(
            id=db_order.id,
            customer_id=db_order.customer_id,
            status=OrderStatus(db_order.status),
            items=[...],
        )
```

```python
# ④ presentation/views.py — DRF view injects dependencies
from rest_framework.views import APIView
from rest_framework.response import Response
from order.application.use_cases.create_order import CreateOrderUseCase
from order.infrastructure.repositories import DjangoOrderRepository
from order.infrastructure.event_publisher import RabbitMQEventPublisher

class CreateOrderView(APIView):
    def post(self, request):
        use_case = CreateOrderUseCase(
            order_repo=DjangoOrderRepository(),
            event_publisher=RabbitMQEventPublisher(),
        )
        input_dto = CreateOrderInput(
            customer_id=request.META["HTTP_X_USER_ID"],
            items=request.data["items"],
        )
        output = use_case.execute(input_dto)
        return Response({"order_id": str(output.order_id), "status": output.status}, status=201)
```

**Dependency rule enforcement:**

| Layer | May Import From | Must NOT Import From |
|-------|----------------|---------------------|
| Domain | Python stdlib only | Django, DRF, any framework |
| Application | Domain | Infrastructure, Presentation, Django |
| Infrastructure | Domain, Application, Django ORM | Presentation |
| Presentation | Application, Domain DTOs, DRF | Infrastructure (directly) |

**Enforcement**: Add a CI linting step with `import-linter`:
```ini
# .importlinter config
[importlinter:contract:domain-purity]
name = Domain layer must not import Django
type = forbidden
source_modules = order.domain
forbidden_modules = django, rest_framework
```

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| **Flat Django structure** (models.py, views.py, serializers.py) | No layer separation; domain logic bleeds into views and models. Violates constitution's Clean Architecture mandate. |
| **Separate Python packages per layer** (pip-installable) | Over-engineered for 7 services. Creates 28+ packages to manage. Convention-based packages within each app achieves the same separation. |
| **Django apps per layer** (domain app, infrastructure app, etc.) | Django apps are intended for feature boundaries, not layer boundaries. Creates migration conflicts and circular import issues. |
| **Hexagonal Architecture (ports/adapters naming)** | Functionally identical to Clean Architecture. "Ports and adapters" naming is less clear than "domain/application/infrastructure/presentation" for teams familiar with the Clean Architecture terminology. |

---

## 3. Inter-Service Communication Patterns

### Decision: Celery + RabbitMQ for Async Events; httpx for Sync Queries

Use **Celery 5.x with RabbitMQ** as the message broker for all asynchronous inter-service events. Use **topic exchanges** for event routing. Use **httpx** for the rare synchronous cross-service query (e.g., gateway proxying). Publish domain events as Celery tasks routed through RabbitMQ topic exchanges.

### Rationale

**Why Celery over raw pika/aio-pika?**

| Factor | Celery + RabbitMQ | Raw pika | aio-pika |
|--------|-------------------|----------|----------|
| **Django integration** | First-class via `django-celery-results`, `django-celery-beat` | Manual — must manage connections, channels, consumers | Manual — requires async Django (ASGI) everywhere |
| **Task retry / backoff** | Built-in (`autoretry_for`, `retry_backoff`) | Manual implementation | Manual implementation |
| **Dead-letter queues** | Built-in (`task_reject_on_worker_lost`, `task_acks_late`) | Manual RabbitMQ DLX config | Manual RabbitMQ DLX config |
| **Monitoring** | Flower dashboard, `celery inspect` | None built-in | None built-in |
| **Serialization** | JSON (default), msgpack, protobuf | Manual | Manual |
| **Worker management** | Multi-process/thread workers, autoscaling, priority queues | Manual consumer loops | Manual consumer loops |
| **Learning curve** | Low — well-documented, massive community | Medium — RabbitMQ concepts required | High — async Python + RabbitMQ concepts |
| **Idempotency support** | `celery-idempotency` or custom `task_id`-based dedup | Manual | Manual |

**Topic exchange pattern:**

```
Exchange: mango.events (type: topic)

Routing keys:
  order.confirmed      → Email queue, Reward queue, Inventory queue
  order.cancelled      → Email queue, Reward queue (reversal), Inventory queue (restock)
  order.shipped        → Email queue
  user.registered      → Email queue (welcome email)
  inventory.updated    → Product queue (availability status)
  payment.completed    → Order queue (confirm order)
  payment.failed       → Order queue (mark failed), Email queue (notify customer)
```

```python
# shared_events/events.py — shared event definitions (lightweight package used by all services)
from dataclasses import dataclass, asdict
from datetime import datetime
from decimal import Decimal
from uuid import UUID
import json

@dataclass(frozen=True)
class DomainEvent:
    event_id: str          # UUID — used for idempotency
    event_type: str        # e.g., "order.confirmed"
    timestamp: str         # ISO 8601
    correlation_id: str    # Trace across services

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass(frozen=True)
class OrderConfirmedEvent(DomainEvent):
    event_type: str = "order.confirmed"
    order_id: str = ""
    customer_id: str = ""
    customer_email: str = ""
    total: str = "0.00"    # String to avoid Decimal serialization issues
    items: list = None     # [{product_id, quantity, unit_price}]
```

```python
# order_service/order/infrastructure/event_publisher.py
from celery import Celery
import json

app = Celery('order_service')
app.config_from_object('django.conf:settings', namespace='CELERY')

class CeleryEventPublisher(EventPublisher):
    def publish(self, event: DomainEvent) -> None:
        """Publish domain event via Celery with topic routing."""
        app.send_task(
            f"handle_{event.event_type.replace('.', '_')}",  # Task name
            args=[event.to_dict()],
            exchange="mango.events",
            routing_key=event.event_type,
            queue=None,  # Routed by topic exchange
        )
```

```python
# email_service/email/infrastructure/tasks.py — consumer side
from celery import shared_task
from email.application.use_cases.send_order_confirmation import SendOrderConfirmationUseCase

@shared_task(
    bind=True,
    name="handle_order_confirmed",
    acks_late=True,                    # Acknowledge only AFTER processing
    reject_on_worker_lost=True,        # Requeue if worker dies
    autoretry_for=(Exception,),        # Auto-retry on any exception
    retry_backoff=True,                # Exponential backoff: 1s, 2s, 4s...
    retry_backoff_max=600,             # Max 10 minutes between retries
    max_retries=5,                     # Then dead-letter
)
def handle_order_confirmed(self, event_data: dict):
    """Idempotent consumer for OrderConfirmed events."""
    event_id = event_data["event_id"]

    # Idempotency check: skip if already processed
    if ProcessedEvent.objects.filter(event_id=event_id).exists():
        return {"status": "skipped", "reason": "already_processed"}

    use_case = SendOrderConfirmationUseCase(...)
    use_case.execute(event_data)

    # Mark as processed (idempotency record)
    ProcessedEvent.objects.create(event_id=event_id, event_type="order.confirmed")
    return {"status": "processed"}
```

**At-least-once delivery guarantee:**

1. **Producer side**: Celery publishes with `acks_late=True` on the consumer — the message stays in RabbitMQ until the consumer explicitly acknowledges.
2. **RabbitMQ**: Durable queues + persistent messages (Celery default with `task_serializer='json'`).
3. **Consumer side**: `acks_late=True` + `reject_on_worker_lost=True` ensures messages re-enter the queue on worker crash.
4. **Idempotency**: Every event has a unique `event_id`. Consumers check a `ProcessedEvent` table before processing. This handles the "at-least-once" duplicate scenario.

**Dead-letter queue configuration:**

```python
# celery_config.py — shared Celery configuration
CELERY_BROKER_URL = "amqp://guest:guest@rabbitmq:5672//"
CELERY_RESULT_BACKEND = "django-db"
CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True

# Dead-letter queue config
CELERY_TASK_QUEUES = {
    "email_events": {
        "exchange": "mango.events",
        "exchange_type": "topic",
        "routing_key": "order.#",  # Bind to all order events
        "queue_arguments": {
            "x-dead-letter-exchange": "mango.dead_letter",
            "x-dead-letter-routing-key": "dead.email",
        },
    },
}
```

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| **Raw pika** | Too low-level. Manual connection management, channel handling, consumer loops, retry logic, and serialization. Celery provides all of this out-of-box. |
| **aio-pika (async)** | Requires ASGI Django throughout. Our services use WSGI (standard Django). Async benefits are marginal for background task processing. |
| **Kafka** | Massive operational overhead for a 7-service platform. Kafka shines at 100k+ events/second. Our scale is orders of magnitude smaller. RabbitMQ is simpler and sufficient. |
| **Redis Streams** | Less mature message broker features than RabbitMQ. No built-in dead-letter queues. Redis is better suited for caching (which we use it for). |
| **AWS SQS/SNS** | Cloud vendor lock-in. Doesn't work in local Docker Compose development without LocalStack. |
| **gRPC for sync** | Adds protobuf compilation step, another serialization format, another set of libraries. httpx + JSON is sufficient for the few sync calls needed. |

---

## 4. Database Strategy

### Decision: Shared PostgreSQL Instance with Separate Schemas (Dev); Separate Instances (Prod)

**Development**: One PostgreSQL 16 container with **7 separate schemas** (one per service) — `auth_schema`, `product_schema`, `cart_schema`, etc. Each service's Django `DATABASES` setting points to its own schema.

**Production**: Separate PostgreSQL instances (or managed databases) per service for true isolation.

### Rationale

**Dev: Shared instance, separate schemas**
- Running 7+ PostgreSQL containers locally consumes ~3.5GB RAM minimum. A single container uses ~500MB.
- Docker Compose setup is dramatically simpler (1 db service vs. 7).
- Schema-level isolation prevents accidental cross-service queries while sharing one connection.
- Migrations run independently per schema — services don't interfere.

**Prod: Separate instances**
- Independent scaling (Order DB might need more IOPS than Email DB).
- Failure isolation (one DB crash doesn't take down all services).
- Independent backup/restore schedules.
- Security isolation (different credentials, different network rules).

**Django configuration:**

```python
# order_service/config/settings.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST", "postgres"),        # shared in dev
        "PORT": os.environ.get("DB_PORT", "5432"),
        "NAME": os.environ.get("DB_NAME", "mango_dev"),       # shared DB in dev
        "USER": os.environ.get("DB_USER", "order_service"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "order_secret"),
        "OPTIONS": {
            "options": f"-c search_path={os.environ.get('DB_SCHEMA', 'order_schema')},public"
        },
    }
}
```

```sql
-- init-db.sql (run on first docker-compose up)
CREATE SCHEMA IF NOT EXISTS auth_schema;
CREATE SCHEMA IF NOT EXISTS product_schema;
CREATE SCHEMA IF NOT EXISTS cart_schema;
CREATE SCHEMA IF NOT EXISTS order_schema;
CREATE SCHEMA IF NOT EXISTS coupon_schema;
CREATE SCHEMA IF NOT EXISTS reward_schema;
CREATE SCHEMA IF NOT EXISTS email_schema;

-- Service-specific users with schema-limited access
CREATE USER auth_service WITH PASSWORD 'auth_secret';
GRANT USAGE, CREATE ON SCHEMA auth_schema TO auth_service;
ALTER DEFAULT PRIVILEGES IN SCHEMA auth_schema GRANT ALL ON TABLES TO auth_service;
-- Repeat for each service...
```

**Migration strategy:**

Each service runs its own migrations independently:

```bash
# In each service's Docker entrypoint
python manage.py migrate --database=default
```

Migrations are forward-only (per constitution). Destructive changes require a 3-step migration plan:
1. **Expand**: Add new column/table alongside old one.
2. **Migrate**: Backfill data, switch application code.
3. **Contract**: Remove old column/table in a subsequent release.

**Cross-service data references:**

Services reference data from other services using **IDs only** (UUIDs). They **never join across service boundaries**. Three patterns:

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **ID reference + denormalized snapshot** | Order needs product details at time of purchase | Order stores `product_id`, `product_name`, `unit_price` — snapshot at order creation time |
| **Synchronous API call** | Cart needs current product price/availability | Cart service calls `GET /api/products/{id}` via internal URL (not through gateway) |
| **Event-driven sync** | Reward service needs to know about user registration | Listens for `user.registered` event and creates a RewardAccount |

```python
# order_service/order/domain/entities.py — stores snapshot, not foreign key
@dataclass
class OrderItem:
    product_id: UUID       # Reference only — no FK to Product DB
    product_name: str      # Denormalized at order creation
    unit_price: Decimal    # Denormalized at order creation
    quantity: int
```

**Internal service-to-service calls (for sync queries):**

```python
# cart_service/cart/infrastructure/product_client.py
import httpx

class ProductServiceClient:
    """Synchronous call to Product service for current data."""
    BASE_URL = "http://product-service:8000/api/products"

    async def get_product(self, product_id: str) -> dict | None:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{self.BASE_URL}/{product_id}/")
            if response.status_code == 200:
                return response.json()
            return None
```

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| **Separate PostgreSQL containers in dev** | 7 containers × ~512MB each = ~3.5GB RAM just for databases. Overkill for local development. Adds complexity to docker-compose with 7 db services. |
| **Shared DB, shared schema (different table prefixes)** | No actual isolation. A bug in one service's migration could corrupt another service's tables. No schema-level permissions. |
| **SQLite in dev** | Different behavior from PostgreSQL (no schemas, different SQL dialect, no JSONB). Tests wouldn't catch real production bugs. |
| **Shared read replicas** | Not needed at our scale. Adds operational complexity. Revisit when any single service exceeds single-instance read capacity. |

---

## 5. Authentication Flow

### Decision: JWT Access + Refresh Tokens via djangorestframework-simplejwt; Gateway Validates; httpOnly Cookies for Next.js

**Auth service** issues JWTs. **Gateway** validates access tokens on every request and injects user context headers. **Downstream services** trust gateway-injected headers. **Next.js frontend** stores tokens in **httpOnly secure cookies** (not localStorage).

### Rationale

**Token architecture:**

```
┌──────────────┐         ┌─────────────┐         ┌──────────────┐
│   Next.js    │ ──(1)──▶│   Gateway   │ ──(3)──▶│ Auth Service │
│   Browser    │         │             │         │              │
│              │ ◀──(2)──│  JWT valid? │         │ Issue tokens │
│ httpOnly     │         │  ↓ Yes      │         │ Refresh flow │
│ cookies      │         │  Inject     │         │ User CRUD    │
│              │         │  X-User-ID  │         └──────────────┘
│              │         │  X-User-Role│         ┌──────────────┐
│              │         │ ──(4)──────▶│──────▶  │ Downstream   │
│              │         │             │         │ Services     │
└──────────────┘         └─────────────┘         └──────────────┘
```

**Flow details:**

**1. Login:**
```
POST /api/auth/login/
Body: {"email": "user@example.com", "password": "..."}

Response (from Auth service, proxied through Gateway):
Set-Cookie: access_token=eyJ...; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=900
Set-Cookie: refresh_token=eyJ...; HttpOnly; Secure; SameSite=Lax; Path=/api/auth/refresh/; Max-Age=604800
Body: {"user": {"id": "...", "email": "...", "role": "customer"}}
```

**2. Authenticated request:**
```
GET /api/orders/                     ← Browser sends access_token cookie automatically
Gateway: Extract token from cookie → Validate with simplejwt → Inject headers
   → X-User-ID: 123e4567-e89b-...
   → X-User-Role: customer
Forwarded to: http://order-service:8000/api/orders/  (with X-User-* headers)
```

**3. Token refresh (access token expired):**
```
POST /api/auth/refresh/              ← Browser sends refresh_token cookie automatically
Gateway: Forward to Auth service (no JWT validation on this endpoint)
Auth service: Validate refresh token → Issue new access + refresh tokens
Response:
Set-Cookie: access_token=eyJ...(new); HttpOnly; Secure; SameSite=Lax; Max-Age=900
Set-Cookie: refresh_token=eyJ...(new); HttpOnly; Secure; SameSite=Lax; Max-Age=604800
```

**4. Next.js middleware handles refresh automatically:**
```typescript
// middleware.ts — runs on every request
import { NextRequest, NextResponse } from 'next/server';

export async function middleware(request: NextRequest) {
  const accessToken = request.cookies.get('access_token');

  if (!accessToken && request.cookies.get('refresh_token')) {
    // Access token expired, refresh token exists — attempt refresh
    const refreshResponse = await fetch(`${API_URL}/api/auth/refresh/`, {
      method: 'POST',
      headers: { Cookie: `refresh_token=${request.cookies.get('refresh_token')?.value}` },
    });

    if (refreshResponse.ok) {
      // Forward the new cookies from the refresh response
      const response = NextResponse.next();
      refreshResponse.headers.getSetCookie().forEach(cookie => {
        response.headers.append('Set-Cookie', cookie);
      });
      return response;
    } else {
      // Refresh failed — redirect to login
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }

  return NextResponse.next();
}
```

**Token configuration (Auth service):**

```python
# auth_service/config/settings.py
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,          # New refresh token on each refresh
    "BLACKLIST_AFTER_ROTATION": True,        # Old refresh token invalidated
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": os.environ["JWT_SECRET_KEY"],  # Shared with Gateway
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "TOKEN_OBTAIN_SERIALIZER": "auth.presentation.serializers.CustomTokenObtainSerializer",
}
```

**Custom token claims (include role):**

```python
# auth_service/auth/presentation/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role       # Add role claim to JWT
        token["email"] = user.email     # Add email claim
        return token
```

**Gateway token validation:**

```python
# gateway/middleware.py
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

class GatewayJWTMiddleware:
    """Validates JWT and injects user context for downstream services."""

    EXEMPT_PATHS = [
        "/api/auth/login/",
        "/api/auth/register/",
        "/api/auth/refresh/",
        "/api/products/",          # Public browsing
    ]

    def __call__(self, request):
        if self._is_exempt(request.path):
            return self.get_response(request)

        token = request.COOKIES.get("access_token")
        if not token:
            return JsonResponse({"error": "Authentication required"}, status=401)

        try:
            validated = AccessToken(token)
            request.META["HTTP_X_USER_ID"] = str(validated["user_id"])
            request.META["HTTP_X_USER_ROLE"] = validated.get("role", "customer")
            request.META["HTTP_X_USER_EMAIL"] = validated.get("email", "")
        except TokenError:
            return JsonResponse({"error": "Invalid or expired token"}, status=401)

        return self.get_response(request)
```

**Downstream services trust gateway headers:**

```python
# Shared mixin for all downstream services
class GatewayAuthMixin:
    """Extract user context from gateway-injected headers."""

    def get_user_id(self, request) -> str:
        user_id = request.META.get("HTTP_X_USER_ID")
        if not user_id:
            raise PermissionDenied("Missing user context")
        return user_id

    def get_user_role(self, request) -> str:
        return request.META.get("HTTP_X_USER_ROLE", "customer")
```

**Security considerations:**
- **httpOnly cookies**: Cannot be accessed by JavaScript — immune to XSS token theft.
- **Secure flag**: Cookies only sent over HTTPS (enable in production).
- **SameSite=Lax**: Prevents CSRF for non-GET requests while allowing normal navigation.
- **Short access token lifetime** (15 min): Limits exposure window if token is somehow compromised.
- **Refresh token rotation**: Each refresh issues a new refresh token and blacklists the old one, preventing reuse.
- **Gateway-only validation**: Downstream services don't need the JWT secret — they trust the gateway headers. This means the JWT secret is only shared between Auth service and Gateway.
- **Internal network only**: Downstream services are not exposed to the internet; only the Gateway is.

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| **localStorage for tokens** | Vulnerable to XSS. Any injected script can steal tokens. httpOnly cookies are fundamentally more secure. |
| **Session-based auth (Django sessions)** | Doesn't work across microservices without a shared session store. JWTs are self-contained and stateless — perfect for microservices. |
| **OAuth2 / OpenID Connect (Keycloak)** | Massive operational overhead for a platform where we control both the frontend and all services. OAuth2 is designed for third-party auth delegation. |
| **Each service validates JWT independently** | Requires distributing the JWT secret to all 7 services. Increases attack surface. Central gateway validation is simpler and more secure. |
| **API key per service** | No user identity tied to keys. Designed for service-to-service auth, not end-user auth. |
| **Paseto tokens** | Less ecosystem support than JWT. simplejwt is mature, well-maintained, and Django-native. |

---

## 6. Payment Integration

### Decision: Stripe via a Dedicated Payment Abstraction in Order Service; Webhook Handler as Separate Endpoint

Integrate **Stripe** using the `stripe` Python SDK directly within the **Order service** (not a separate Payment microservice). Use **Stripe Checkout Sessions** (redirect flow) for payment. Handle **Stripe webhooks** via a dedicated endpoint on the Order service.

### Rationale

**Why not a separate Payment service?**

A Payment service would own payment state (charges, refunds, payment methods). But in our platform:
- Payment is tightly coupled to order lifecycle (payment → confirm order → trigger events).
- Only one entity creates payments: Orders.
- We'd need synchronous communication between Order service and Payment service for every checkout — adding latency and a failure point.
- A separate service only makes sense when multiple services create payments (e.g., subscriptions + one-time purchases + marketplace payouts). We have none of that.

Placing Stripe integration in the Order service's **infrastructure layer** keeps it cleanly separated (behind an interface) while avoiding unnecessary network hops.

**Why Stripe?**

| Factor | Stripe | PayPal | Square | Razorpay |
|--------|--------|--------|--------|----------|
| **Python SDK quality** | Excellent (`stripe` package, well-typed) | Mediocre (REST SDK, verbose) | Good | Good (India-focused) |
| **Checkout flow** | Stripe Checkout (hosted) or PaymentIntents (embedded) | Redirect-heavy | Limited hosted option | Dashboard-heavy |
| **Webhook support** | Excellent, with signature verification | Good | Good | Good |
| **Test mode** | Comprehensive test keys, test cards, CLI for local webhooks | Sandbox environment | Sandbox | Test mode |
| **Django community** | Massive — `dj-stripe`, many tutorials | Moderate | Small | Moderate |
| **Documentation** | Industry-leading | Average | Good | Good |
| **Pricing** | 2.9% + $0.30 | 2.9% + $0.30 | 2.6% + $0.10 | 2% (India) |

**Architecture:**

```python
# order/domain/interfaces.py — payment gateway abstraction
from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class PaymentIntent:
    checkout_url: str        # URL to redirect user to payment page
    session_id: str          # Provider's session/payment ID
    status: str              # "pending", "completed", "failed"

class PaymentGateway(ABC):
    @abstractmethod
    def create_checkout_session(
        self,
        order_id: str,
        items: list[dict],         # [{name, quantity, unit_price}]
        total: Decimal,
        customer_email: str,
        success_url: str,
        cancel_url: str,
    ) -> PaymentIntent: ...

    @abstractmethod
    def verify_webhook_signature(self, payload: bytes, signature: str) -> dict: ...
```

```python
# order/infrastructure/payment_gateway.py — Stripe implementation
import stripe
from order.domain.interfaces import PaymentGateway, PaymentIntent

class StripePaymentGateway(PaymentGateway):
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    def create_checkout_session(self, order_id, items, total, customer_email, success_url, cancel_url):
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            customer_email=customer_email,
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": item["name"]},
                        "unit_amount": int(item["unit_price"] * 100),  # Cents
                    },
                    "quantity": item["quantity"],
                }
                for item in items
            ],
            metadata={"order_id": order_id},
            success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=cancel_url,
        )
        return PaymentIntent(
            checkout_url=session.url,
            session_id=session.id,
            status="pending",
        )

    def verify_webhook_signature(self, payload, signature):
        return stripe.Webhook.construct_event(
            payload, signature, settings.STRIPE_WEBHOOK_SECRET
        )
```

**Checkout flow:**

```
1. User clicks "Place Order" in Next.js frontend
2. Frontend: POST /api/orders/checkout/
3. Gateway → Order service:
   a. Create Order entity (status: PENDING)
   b. Call StripePaymentGateway.create_checkout_session()
   c. Save Stripe session_id on Order
   d. Return {checkout_url: "https://checkout.stripe.com/..."}
4. Frontend: Redirect user to Stripe Checkout page
5. User completes payment on Stripe
6. Stripe redirects user to success_url (Next.js /orders/confirmation?session_id=...)
7. Stripe fires webhook → POST /api/orders/webhooks/stripe/
```

**Webhook handler:**

```python
# order/presentation/views.py
class StripeWebhookView(APIView):
    """Handles async payment confirmations from Stripe."""
    permission_classes = []  # No auth — Stripe calls this directly
    authentication_classes = []

    def post(self, request):
        payload = request.body
        signature = request.META.get("HTTP_STRIPE_SIGNATURE")

        payment_gateway = StripePaymentGateway()
        try:
            event = payment_gateway.verify_webhook_signature(payload, signature)
        except ValueError:
            return Response(status=400)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            order_id = session["metadata"]["order_id"]

            # Use case: confirm order + publish events
            use_case = ConfirmOrderUseCase(
                order_repo=DjangoOrderRepository(),
                event_publisher=CeleryEventPublisher(),
            )
            use_case.execute(order_id=order_id, payment_session_id=session["id"])

        return Response(status=200)
```

**Local development with Stripe webhooks:**

```bash
# Use Stripe CLI to forward webhooks to local Docker service
stripe listen --forward-to localhost:8003/api/orders/webhooks/stripe/
```

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| **Separate Payment microservice** | Over-engineering. Only Orders create payments. A separate service adds network hop, sync communication overhead, and distributed transaction complexity with no compensating benefit. |
| **PayPal** | Worse developer experience, redirect-heavy checkout flow, mediocre Python SDK. |
| **Stripe PaymentIntents (embedded)** | More complex frontend integration (Stripe.js Elements). Checkout Sessions are simpler, hosted by Stripe, PCI burden is near-zero. Embedded can be a future enhancement. |
| **dj-stripe (Django library)** | Adds heavy Django model layer that mirrors Stripe's data. Useful for SaaS subscriptions but overkill for one-time e-commerce payments. We only need Checkout Sessions + Webhooks. |
| **Braintree** | Owned by PayPal. Less developer-friendly than Stripe. Smaller community. |

---

## 7. Next.js Frontend Architecture

### Decision: App Router with Server Components Default; React Context for Cart; httpOnly Cookie Auth; API Route Handlers for BFF

Use **Next.js 14+ App Router** with **Server Components as default** for product browsing (SEO + performance). **Client Components** only for interactive elements (cart, forms, modals). **React Context** for cart state. **httpOnly cookies** for auth (set by backend). **Route Handlers** (`app/api/`) as a Backend-for-Frontend (BFF) layer.

### Rationale

**Component strategy:**

| Area | Component Type | Why |
|------|---------------|-----|
| Product listing page | **Server Component** | SEO-critical, data-heavy. Fetched on server, streamed to client. Zero client JS. |
| Product detail page | **Server Component** | SEO-critical. Static-renderable for popular products (`generateStaticParams`). |
| Search/filter bar | **Client Component** | User interaction (typing, filtering). Uses `useSearchParams`. |
| Shopping cart sidebar | **Client Component** | Highly interactive (quantity changes, remove items). Real-time subtotal. |
| Checkout form | **Client Component** | Form state, validation, Stripe redirect. |
| Order history page | **Server Component** | Read-only data, fetched on server. Authenticated via cookie forwarding. |
| Navigation bar | **Client Component** | Shows cart count (reactive), user avatar (auth state). |
| Admin dashboard | **Client Component** | CRUD operations, forms, modals. |
| Auth forms (login/register) | **Client Component** | Form state, validation, redirect after submit. |

**Project structure:**

```
frontend/
├── app/
│   ├── layout.tsx                   # Root layout — cart provider, auth context
│   ├── page.tsx                     # Homepage (Server Component)
│   ├── (shop)/                      # Route group for public storefront
│   │   ├── products/
│   │   │   ├── page.tsx             # Product listing (Server Component)
│   │   │   └── [slug]/
│   │   │       └── page.tsx         # Product detail (Server Component)
│   │   ├── cart/
│   │   │   └── page.tsx             # Cart page (Client Component wrapper)
│   │   └── checkout/
│   │       └── page.tsx             # Checkout (Client Component)
│   ├── (auth)/                      # Route group for auth pages
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
│   ├── (account)/                   # Route group for authenticated pages
│   │   ├── orders/
│   │   │   └── page.tsx             # Order history (Server Component)
│   │   └── rewards/
│   │       └── page.tsx             # Rewards dashboard (Server Component)
│   ├── admin/                       # Admin area
│   │   ├── layout.tsx               # Admin layout with sidebar
│   │   ├── products/
│   │   └── coupons/
│   └── api/                         # BFF Route Handlers
│       ├── cart/
│       │   └── route.ts             # Cart API (proxies to Gateway, manages optimistic updates)
│       └── auth/
│           └── route.ts             # Auth helpers (cookie management)
├── components/
│   ├── ui/                          # Shared UI primitives (Button, Modal, Input)
│   ├── product/
│   │   ├── ProductCard.tsx          # Server Component
│   │   ├── ProductGrid.tsx          # Server Component
│   │   └── AddToCartButton.tsx      # Client Component
│   ├── cart/
│   │   ├── CartProvider.tsx         # Client Component — React Context
│   │   ├── CartSidebar.tsx          # Client Component
│   │   └── CartItem.tsx             # Client Component
│   └── layout/
│       ├── Navbar.tsx               # Client Component (cart count, auth state)
│       └── Footer.tsx               # Server Component
├── lib/
│   ├── api.ts                       # API client (fetch wrapper with cookie forwarding)
│   ├── types.ts                     # Shared TypeScript types
│   └── utils.ts                     # Utility functions
├── middleware.ts                     # Auth token refresh, protected route redirect
└── next.config.ts
```

**Cart state management with React Context:**

```typescript
// components/cart/CartProvider.tsx
"use client";

import { createContext, useContext, useReducer, useEffect } from "react";

interface CartItem {
  productId: string;
  name: string;
  price: number;
  quantity: number;
  imageUrl: string;
}

interface CartState {
  items: CartItem[];
  isLoading: boolean;
}

type CartAction =
  | { type: "SET_CART"; items: CartItem[] }
  | { type: "ADD_ITEM"; item: CartItem }
  | { type: "UPDATE_QUANTITY"; productId: string; quantity: number }
  | { type: "REMOVE_ITEM"; productId: string }
  | { type: "CLEAR" };

const CartContext = createContext<{
  state: CartState;
  addItem: (item: CartItem) => Promise<void>;
  updateQuantity: (productId: string, quantity: number) => Promise<void>;
  removeItem: (productId: string) => Promise<void>;
  subtotal: number;
} | null>(null);

function cartReducer(state: CartState, action: CartAction): CartState {
  switch (action.type) {
    case "SET_CART":
      return { ...state, items: action.items, isLoading: false };
    case "ADD_ITEM": {
      const existing = state.items.find(i => i.productId === action.item.productId);
      if (existing) {
        return {
          ...state,
          items: state.items.map(i =>
            i.productId === action.item.productId
              ? { ...i, quantity: i.quantity + action.item.quantity }
              : i
          ),
        };
      }
      return { ...state, items: [...state.items, action.item] };
    }
    case "UPDATE_QUANTITY":
      return {
        ...state,
        items: state.items.map(i =>
          i.productId === action.productId ? { ...i, quantity: action.quantity } : i
        ),
      };
    case "REMOVE_ITEM":
      return { ...state, items: state.items.filter(i => i.productId !== action.productId) };
    case "CLEAR":
      return { ...state, items: [] };
    default:
      return state;
  }
}

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(cartReducer, { items: [], isLoading: true });

  // Hydrate cart from backend on mount
  useEffect(() => {
    fetch("/api/cart").then(r => r.json()).then(data => {
      dispatch({ type: "SET_CART", items: data.items });
    });
  }, []);

  const addItem = async (item: CartItem) => {
    dispatch({ type: "ADD_ITEM", item });  // Optimistic update
    await fetch("/api/cart", {
      method: "POST",
      body: JSON.stringify({ productId: item.productId, quantity: item.quantity }),
    });
  };

  const subtotal = state.items.reduce((sum, i) => sum + i.price * i.quantity, 0);

  return (
    <CartContext.Provider value={{ state, addItem, updateQuantity, removeItem, subtotal }}>
      {children}
    </CartContext.Provider>
  );
}

export const useCart = () => {
  const ctx = useContext(CartContext);
  if (!ctx) throw new Error("useCart must be used within CartProvider");
  return ctx;
};
```

**Why React Context over Zustand/Redux?**

| Factor | React Context | Zustand | Redux Toolkit |
|--------|--------------|---------|---------------|
| **Bundle size** | 0 KB (built into React) | ~1 KB | ~15 KB |
| **Complexity** | Low — `useReducer` + `useContext` | Low | Medium-high |
| **SSR compatibility** | Native | Good | Good with extra config |
| **Cart-specific needs** | ≤50 items, ≤5 updates/session — trivially sufficient | Optimized for frequent updates | Overkill for simple state |
| **Devtools** | React DevTools | Dedicated devtools | Redux DevTools |

Cart state is simple (list of items + quantities), updates are infrequent (add/remove/change quantity), and re-renders are limited to the cart components. React Context handles this trivially. If performance becomes an issue (unlikely for cart), migrating to Zustand is a 30-minute refactor.

**Server Component data fetching:**

```typescript
// app/(shop)/products/page.tsx — Server Component, zero client JS
import { ProductGrid } from "@/components/product/ProductGrid";

interface Props {
  searchParams: { page?: string; category?: string; q?: string };
}

export default async function ProductsPage({ searchParams }: Props) {
  const params = new URLSearchParams(searchParams as Record<string, string>);
  const response = await fetch(
    `${process.env.GATEWAY_URL}/api/products/?${params}`,
    { next: { revalidate: 60 } }  // ISR: revalidate every 60 seconds
  );
  const data = await response.json();

  return (
    <main>
      <h1>Products</h1>
      <ProductGrid products={data.results} />
      {/* Pagination uses Server Component — no client JS */}
    </main>
  );
}
```

**Auth: Cookie forwarding in Server Components:**

```typescript
// lib/api.ts — server-side fetch with cookie forwarding
import { cookies } from "next/headers";

export async function serverFetch(path: string, options?: RequestInit) {
  const cookieStore = cookies();
  const accessToken = cookieStore.get("access_token")?.value;

  return fetch(`${process.env.GATEWAY_URL}${path}`, {
    ...options,
    headers: {
      ...options?.headers,
      Cookie: `access_token=${accessToken}`,
    },
  });
}

// Usage in a Server Component:
const orders = await serverFetch("/api/orders/").then(r => r.json());
```

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| **Pages Router** | Deprecated architecture in Next.js 14+. App Router is the future. Server Components give measurable performance benefits for product catalog. |
| **Redux Toolkit for cart** | ~15KB bundle overhead for state that is simple and rarely updated. Boilerplate-heavy for the cart use case. |
| **Zustand** | Good library, but unnecessary. Cart state is trivially simple. React Context with `useReducer` is zero-dependency. Zustand becomes worth it only if state complexity grows significantly. |
| **localStorage for auth tokens** | Vulnerable to XSS. Any script injection can steal tokens. httpOnly cookies are the secure standard. |
| **SWR / React Query for data fetching** | Useful for client-side data fetching, but we use Server Components for data-heavy pages (products, orders). Server Components eliminate the need for client-side data fetching libraries for read-heavy pages. SWR/React Query still useful for client-side mutations — can add later. |
| **tRPC** | Designed for TypeScript backends. Our backend is Python/Django. No benefit. |

---

## 8. Docker and Kubernetes Strategy

### Decision: Single docker-compose.yml with Service Profiles; Kubernetes with Helm Charts for Production

**Development**: One `docker-compose.yml` with all services. Use **profiles** to start subsets of services during development. Shared infrastructure (PostgreSQL, RabbitMQ, Redis) as base services. Each Django service has its own Dockerfile.

**Production**: Kubernetes with **Helm charts** per service. One Deployment + Service + HorizontalPodAutoscaler per microservice.

### Rationale

**Docker Compose structure:**

```yaml
# docker-compose.yml
version: "3.9"

x-django-common: &django-common
  build:
    context: .
    dockerfile: docker/django/Dockerfile
  depends_on:
    postgres:
      condition: service_healthy
    rabbitmq:
      condition: service_healthy
    redis:
      condition: service_healthy
  networks:
    - mango-network
  restart: unless-stopped

services:
  # ─── Infrastructure ───────────────────────────────────
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: mango_dev
      POSTGRES_USER: mango_admin
      POSTGRES_PASSWORD: mango_secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./docker/postgres/init-db.sql:/docker-entrypoint-initdb.d/init-db.sql
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U mango_admin -d mango_dev"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - mango-network

  rabbitmq:
    image: rabbitmq:3.13-management-alpine
    environment:
      RABBITMQ_DEFAULT_USER: mango
      RABBITMQ_DEFAULT_PASS: mango_secret
    ports:
      - "5672:5672"      # AMQP
      - "15672:15672"    # Management UI
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
      interval: 10s
      timeout: 10s
      retries: 5
    networks:
      - mango-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/var/lib/redis/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - mango-network

  # ─── API Gateway ──────────────────────────────────────
  gateway:
    <<: *django-common
    build:
      context: .
      dockerfile: docker/django/Dockerfile
      args:
        SERVICE_DIR: gateway
    ports:
      - "8000:8000"
    environment:
      - SERVICE_NAME=gateway
      - DB_SCHEMA=gateway_schema
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    command: >
      gunicorn config.wsgi:application
      --bind 0.0.0.0:8000
      --workers 2
      --timeout 120
      --access-logfile -

  # ─── Microservices ────────────────────────────────────
  auth-service:
    <<: *django-common
    build:
      context: .
      dockerfile: docker/django/Dockerfile
      args:
        SERVICE_DIR: auth_service
    ports:
      - "8001:8000"
    environment:
      - SERVICE_NAME=auth
      - DB_SCHEMA=auth_schema
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
    command: >
      gunicorn config.wsgi:application
      --bind 0.0.0.0:8000
      --workers 2

  product-service:
    <<: *django-common
    build:
      context: .
      dockerfile: docker/django/Dockerfile
      args:
        SERVICE_DIR: product_service
    ports:
      - "8002:8000"
    environment:
      - SERVICE_NAME=product
      - DB_SCHEMA=product_schema
    command: >
      gunicorn config.wsgi:application
      --bind 0.0.0.0:8000
      --workers 2

  cart-service:
    <<: *django-common
    build:
      context: .
      dockerfile: docker/django/Dockerfile
      args:
        SERVICE_DIR: cart_service
    ports:
      - "8003:8000"
    environment:
      - SERVICE_NAME=cart
      - DB_SCHEMA=cart_schema
      - REDIS_URL=redis://redis:6379/1
    command: >
      gunicorn config.wsgi:application
      --bind 0.0.0.0:8000
      --workers 2

  order-service:
    <<: *django-common
    build:
      context: .
      dockerfile: docker/django/Dockerfile
      args:
        SERVICE_DIR: order_service
    ports:
      - "8004:8000"
    environment:
      - SERVICE_NAME=order
      - DB_SCHEMA=order_schema
      - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
      - STRIPE_WEBHOOK_SECRET=${STRIPE_WEBHOOK_SECRET}
    command: >
      gunicorn config.wsgi:application
      --bind 0.0.0.0:8000
      --workers 2

  coupon-service:
    <<: *django-common
    build:
      context: .
      dockerfile: docker/django/Dockerfile
      args:
        SERVICE_DIR: coupon_service
    ports:
      - "8005:8000"
    environment:
      - SERVICE_NAME=coupon
      - DB_SCHEMA=coupon_schema
    command: >
      gunicorn config.wsgi:application
      --bind 0.0.0.0:8000
      --workers 2

  reward-service:
    <<: *django-common
    build:
      context: .
      dockerfile: docker/django/Dockerfile
      args:
        SERVICE_DIR: reward_service
    ports:
      - "8006:8000"
    environment:
      - SERVICE_NAME=reward
      - DB_SCHEMA=reward_schema
    command: >
      gunicorn config.wsgi:application
      --bind 0.0.0.0:8000
      --workers 2

  email-service:
    <<: *django-common
    build:
      context: .
      dockerfile: docker/django/Dockerfile
      args:
        SERVICE_DIR: email_service
    ports:
      - "8007:8000"
    environment:
      - SERVICE_NAME=email
      - DB_SCHEMA=email_schema
      - EMAIL_HOST=${EMAIL_HOST:-mailpit}
      - EMAIL_PORT=${EMAIL_PORT:-1025}
    command: >
      gunicorn config.wsgi:application
      --bind 0.0.0.0:8000
      --workers 1

  # ─── Celery Workers ──────────────────────────────────
  celery-order-worker:
    <<: *django-common
    build:
      context: .
      dockerfile: docker/django/Dockerfile
      args:
        SERVICE_DIR: order_service
    environment:
      - SERVICE_NAME=order
      - DB_SCHEMA=order_schema
    command: >
      celery -A config worker
      --loglevel=info
      --queues=order_events
      --concurrency=2
    depends_on:
      - order-service

  celery-email-worker:
    <<: *django-common
    build:
      context: .
      dockerfile: docker/django/Dockerfile
      args:
        SERVICE_DIR: email_service
    environment:
      - SERVICE_NAME=email
      - DB_SCHEMA=email_schema
    command: >
      celery -A config worker
      --loglevel=info
      --queues=email_events
      --concurrency=2
    depends_on:
      - email-service

  celery-reward-worker:
    <<: *django-common
    build:
      context: .
      dockerfile: docker/django/Dockerfile
      args:
        SERVICE_DIR: reward_service
    environment:
      - SERVICE_NAME=reward
      - DB_SCHEMA=reward_schema
    command: >
      celery -A config worker
      --loglevel=info
      --queues=reward_events
      --concurrency=2
    depends_on:
      - reward-service

  flower:
    <<: *django-common
    build:
      context: .
      dockerfile: docker/django/Dockerfile
      args:
        SERVICE_DIR: order_service
    ports:
      - "5555:5555"
    command: celery -A config flower --port=5555
    profiles:
      - monitoring

  # ─── Frontend ─────────────────────────────────────────
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - GATEWAY_URL=http://gateway:8000
      - NEXT_PUBLIC_GATEWAY_URL=http://localhost:8000
    depends_on:
      - gateway
    networks:
      - mango-network

  # ─── Dev Tools ────────────────────────────────────────
  mailpit:
    image: axllent/mailpit:latest
    ports:
      - "8025:8025"     # Web UI
      - "1025:1025"     # SMTP
    profiles:
      - dev-tools
    networks:
      - mango-network

volumes:
  postgres_data:
  rabbitmq_data:
  redis_data:

networks:
  mango-network:
    driver: bridge
```

**Shared Dockerfile (multi-stage):**

```dockerfile
# docker/django/Dockerfile
FROM python:3.12-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ARG SERVICE_DIR
ENV SERVICE_DIR=${SERVICE_DIR}

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==1.8.0
RUN poetry config virtualenvs.create false

# Copy and install dependencies (cached layer)
COPY ${SERVICE_DIR}/pyproject.toml ${SERVICE_DIR}/poetry.lock* ./
RUN poetry install --no-root --no-interaction --no-ansi

# Copy service code
COPY ${SERVICE_DIR}/ .
COPY shared_events/ /app/shared_events/

# Collect static files
RUN python manage.py collectstatic --noinput 2>/dev/null || true

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import httpx; r = httpx.get('http://localhost:8000/health/'); r.raise_for_status()"
```

**Health check endpoint (every service):**

```python
# Shared across all services — config/urls.py includes this
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    """Kubernetes / Docker health check endpoint."""
    checks = {"status": "healthy", "service": os.environ.get("SERVICE_NAME", "unknown")}

    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        checks["database"] = "connected"
    except Exception as e:
        checks["database"] = f"error: {str(e)}"
        checks["status"] = "unhealthy"

    status_code = 200 if checks["status"] == "healthy" else 503
    return JsonResponse(checks, status=status_code)
```

**Development workflow commands:**

```bash
# Start everything
docker compose up -d

# Start only infrastructure + specific service (for focused development)
docker compose up -d postgres rabbitmq redis auth-service gateway frontend

# Start with monitoring tools
docker compose --profile monitoring --profile dev-tools up -d

# Run migrations for a specific service
docker compose exec auth-service python manage.py migrate

# Run tests for a specific service
docker compose exec auth-service pytest

# View logs for a specific service
docker compose logs -f order-service

# Rebuild a single service after code changes
docker compose up -d --build product-service
```

**Kubernetes production considerations:**

```yaml
# k8s/order-service/deployment.yaml (example)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
  labels:
    app: order-service
spec:
  replicas: 2
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
        - name: order-service
          image: mango/order-service:latest
          ports:
            - containerPort: 8000
          envFrom:
            - secretRef:
                name: order-service-secrets
            - configMapRef:
                name: order-service-config
          livenessProbe:
            httpGet:
              path: /health/
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health/
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            requests:
              cpu: 100m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi
---
apiVersion: v1
kind: Service
metadata:
  name: order-service
spec:
  selector:
    app: order-service
  ports:
    - port: 8000
      targetPort: 8000
  type: ClusterIP          # Internal only — gateway is the ingress point
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-service
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

**Production Kubernetes architecture:**

```
Internet → Ingress (NGINX Ingress Controller) → Gateway Service (ClusterIP)
    → Auth Service (ClusterIP)
    → Product Service (ClusterIP)
    → Cart Service (ClusterIP)
    → Order Service (ClusterIP)
    → Coupon Service (ClusterIP)
    → Reward Service (ClusterIP)
    → Email Service (ClusterIP)

Managed services:
    → AWS RDS PostgreSQL (one instance per service, or Aurora Serverless)
    → Amazon MQ for RabbitMQ (or self-hosted via Helm)
    → Amazon ElastiCache for Redis
    → ECR for container images
    → S3 for product images
```

### Alternatives Considered

| Alternative | Rejected Because |
|-------------|-----------------|
| **Separate docker-compose per service** | Fragments the development experience. Developers need to run N compose files. Shared infrastructure (PostgreSQL, RabbitMQ, Redis) would need duplicate definitions or external networks. |
| **Podman / Podman Compose** | Less mature compose support. Docker Compose is the team standard and better documented. |
| **Docker Swarm for production** | Deprecated trajectory. Kubernetes is the industry standard and has superior scaling, rolling updates, and ecosystem. |
| **AWS ECS for production** | Viable alternative. Less portable than Kubernetes. ECS is AWS-only; Kubernetes runs anywhere. |
| **Skaffold for local Kubernetes** | Too complex for local development. Docker Compose is simpler and faster. Kubernetes for production only. |
| **Tilt / DevSpace** | Good tools but add complexity. Docker Compose is sufficient for a 7-service platform. |

---

## Summary Decision Matrix

| Topic | Decision | Key Library/Tool |
|-------|----------|-----------------|
| **1. API Gateway** | Custom Django gateway | `httpx`, `djangorestframework-simplejwt`, `django-ratelimit` |
| **2. Clean Architecture** | 4-layer packages per Django app | `import-linter` (CI enforcement), `dataclasses` (domain entities) |
| **3. Inter-service Comms** | Celery + RabbitMQ (async), httpx (sync) | `celery[rabbitmq]`, `django-celery-results`, `httpx` |
| **4. Database** | Shared PostgreSQL + separate schemas (dev); separate instances (prod) | `postgresql:16-alpine`, Django schema config via `search_path` |
| **5. Authentication** | JWT in httpOnly cookies; gateway validates; X-User-* headers downstream | `djangorestframework-simplejwt` |
| **6. Payment** | Stripe in Order service infrastructure layer | `stripe` Python SDK, Stripe Checkout Sessions |
| **7. Frontend** | Next.js 14+ App Router, Server Components default, React Context for cart | `next`, React Context + `useReducer` |
| **8. Docker/K8s** | Single docker-compose.yml with profiles (dev); Kubernetes + Helm (prod) | Docker Compose 3.9, `gunicorn`, per-service Dockerfiles |
