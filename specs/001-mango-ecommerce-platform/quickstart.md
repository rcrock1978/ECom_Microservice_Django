# Quickstart Guide: Mango Microservices E-Commerce Platform

**Created**: 2026-03-04  
**Feature**: 001-mango-ecommerce-platform

## Prerequisites

- Python 3.12+
- Node.js 20+ and pnpm 9+
- Docker Desktop (Docker Compose V2)
- Git

## 1. Clone and Setup

```bash
git clone https://github.com/rcrock1978/ECom_Microservice_Django.git
cd ECom_Microservice_Django
git checkout 001-mango-ecommerce-platform
```

## 2. Start Infrastructure (One Command)

```bash
docker compose up -d
```

This starts all services:
- 7 Django microservices (auth, product, cart, order, coupon, reward, email)
- 1 Django API gateway
- 1 Next.js frontend
- PostgreSQL 16
- RabbitMQ 3.13 (management UI at http://localhost:15672)
- Redis 7

## 3. Verify Services

```bash
# Check all containers are healthy
docker compose ps

# Expected output: all services showing "healthy"
```

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Next.js storefront |
| Gateway | http://localhost:8080 | API Gateway |
| Auth Service | http://localhost:8001 | Authentication (internal) |
| Product Service | http://localhost:8002 | Product catalog (internal) |
| Cart Service | http://localhost:8003 | Shopping cart (internal) |
| Order Service | http://localhost:8004 | Orders (internal) |
| Coupon Service | http://localhost:8005 | Coupons (internal) |
| Reward Service | http://localhost:8006 | Rewards (internal) |
| Email Service | http://localhost:8007 | Email processing (internal) |
| RabbitMQ UI | http://localhost:15672 | Message broker dashboard |
| pgAdmin | http://localhost:5050 | Database management (optional) |

## 4. Run Migrations

```bash
# Run migrations for all services
docker compose exec auth-service python manage.py migrate
docker compose exec product-service python manage.py migrate
docker compose exec cart-service python manage.py migrate
docker compose exec order-service python manage.py migrate
docker compose exec coupon-service python manage.py migrate
docker compose exec reward-service python manage.py migrate
docker compose exec email-service python manage.py migrate
```

## 5. Seed Initial Data

```bash
# Create admin user
docker compose exec auth-service python manage.py createsuperuser

# Seed sample products and categories
docker compose exec product-service python manage.py seed_products

# Seed sample coupons
docker compose exec coupon-service python manage.py seed_coupons
```

## 6. Run Tests

```bash
# Run all tests across all services
docker compose exec auth-service pytest
docker compose exec product-service pytest
docker compose exec cart-service pytest
docker compose exec order-service pytest
docker compose exec coupon-service pytest
docker compose exec reward-service pytest
docker compose exec email-service pytest

# Run frontend tests
docker compose exec frontend pnpm test
```

## 7. Local Development (Without Docker)

For working on a single service:

```bash
# Backend service (e.g., product-service)
cd services/product_service
poetry install
poetry run python manage.py runserver 8002

# Frontend
cd frontend
pnpm install
pnpm dev
```

Ensure PostgreSQL, RabbitMQ, and Redis are accessible (can run these via Docker while developing services locally).

## Project Structure

```
ecom_microservices/
├── services/                    # All Django microservices
│   ├── auth_service/            # Mango.Services.AuthAPI
│   ├── product_service/         # Mango.Services.ProductAPI
│   ├── cart_service/            # Mango.Services.ShoppingCartAPI
│   ├── order_service/           # Mango.Services.OrderAPI
│   ├── coupon_service/          # Mango.Services.CouponAPI
│   ├── reward_service/          # Mango.Services.RewardAPI
│   ├── email_service/           # Mango.Services.EmailAPI
│   └── gateway/                 # Mango.GatewaySolution
├── shared/                      # Mango.MessageBus (shared library)
│   ├── message_bus/             # Event publishing/consuming
│   ├── common/                  # Shared utilities, base classes
│   └── testing/                 # Shared test fixtures
├── frontend/                    # Mango.Web (Next.js)
│   ├── src/
│   │   ├── app/                 # Next.js App Router pages
│   │   ├── components/          # React components
│   │   ├── lib/                 # API client, utilities
│   │   └── types/               # TypeScript types
│   └── tests/
├── docker-compose.yml           # Local development orchestration
├── docker-compose.prod.yml      # Production overrides
├── specs/                       # Feature specifications
└── .specify/                    # SpecKit configuration
```

## Environment Variables

Each service reads from `.env` in its directory (not committed to git). See `.env.example` files for required variables.

Key shared environment variables:
```
DATABASE_HOST=localhost
DATABASE_PORT=5432
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=your-secret-key
```
