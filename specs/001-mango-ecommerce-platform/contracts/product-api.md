# API Contracts: Product Service

**Base URL**: `/api/v1/products/` and `/api/v1/categories/`  
**Upstream**: `http://product-service:8000`

---

## GET /api/v1/products/

List products with pagination, filtering, and search.

**Auth Required**: No

**Query Parameters**:
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `page` | int | 1 | Page number |
| `page_size` | int | 20 | Items per page (max 100) |
| `category` | UUID | — | Filter by category ID |
| `search` | string | — | Full-text search on name + description |
| `min_price` | decimal | — | Minimum price filter |
| `max_price` | decimal | — | Maximum price filter |
| `in_stock` | boolean | — | Filter to in-stock only |
| `sort` | string | `-created_at` | Sort field: `price`, `-price`, `name`, `-created_at` |

**Response 200**:
```json
{
  "data": [
    {
      "id": "uuid",
      "name": "Wireless Headphones",
      "slug": "wireless-headphones",
      "description": "High-quality bluetooth headphones...",
      "price": "79.99",
      "category": {"id": "uuid", "name": "Electronics", "slug": "electronics"},
      "image_url": "https://storage.example.com/products/headphones.jpg",
      "stock_quantity": 150,
      "is_in_stock": true
    }
  ],
  "meta": {"page": 1, "page_size": 20, "total": 87}
}
```

---

## GET /api/v1/products/{slug}/

Get product detail by slug.

**Auth Required**: No

**Response 200**:
```json
{
  "data": {
    "id": "uuid",
    "name": "Wireless Headphones",
    "slug": "wireless-headphones",
    "description": "High-quality bluetooth headphones with noise cancellation...",
    "price": "79.99",
    "category": {"id": "uuid", "name": "Electronics", "slug": "electronics"},
    "image_url": "https://storage.example.com/products/headphones.jpg",
    "stock_quantity": 150,
    "is_in_stock": true,
    "created_at": "2026-03-01T10:00:00Z"
  }
}
```

**Response 404**: Product not found

---

## POST /api/v1/products/ (Admin)

Create a new product.

**Auth Required**: Yes (Admin role)

**Request**:
```json
{
  "name": "Wireless Headphones",
  "description": "High-quality bluetooth headphones...",
  "price": "79.99",
  "category_id": "uuid",
  "image_url": "https://storage.example.com/products/headphones.jpg",
  "stock_quantity": 150
}
```

**Response 201**: Created product object  
**Response 400**: Validation error  
**Response 403**: Not admin

---

## PUT /api/v1/products/{id}/ (Admin)

Update a product.

**Auth Required**: Yes (Admin role)

**Request**: Same fields as create (all optional for partial update)  
**Response 200**: Updated product  
**Response 404**: Product not found

---

## DELETE /api/v1/products/{id}/ (Admin)

Delete or deactivate a product.

**Auth Required**: Yes (Admin role)

**Response 204**: Product deleted  
**Response 409**: Product has pending orders — returns suggestion to deactivate

---

## GET /api/v1/categories/

List all active categories.

**Auth Required**: No

**Response 200**:
```json
{
  "data": [
    {
      "id": "uuid",
      "name": "Electronics",
      "slug": "electronics",
      "description": "Electronic devices and accessories",
      "parent_id": null,
      "children": [
        {"id": "uuid", "name": "Audio", "slug": "audio"}
      ]
    }
  ]
}
```

---

## POST /api/v1/categories/ (Admin)

Create a category.

**Auth Required**: Yes (Admin role)

**Request**:
```json
{
  "name": "Audio",
  "description": "Audio equipment",
  "parent_id": "uuid-of-electronics"
}
```

**Response 201**: Created category  
**Response 400**: Validation error (max depth exceeded, duplicate slug)

---

## Internal: GET /internal/products/{id}/

Used by Cart and Order services to fetch current product data (not exposed via gateway).

**Response 200**:
```json
{
  "id": "uuid",
  "name": "Wireless Headphones",
  "price": "79.99",
  "stock_quantity": 150,
  "is_active": true
}
```
