# Software Design Document: E-Commerce Product Catalog API

## Faculty Development Program — AI-Native Software Development

| Field               | Detail                                                    |
|---------------------|-----------------------------------------------------------|
| **Module**          | Hands-on Exercise 2 — E-Commerce Product Catalog API      |
| **Duration**        | 1.5 – 2 hours (practical, instructor-guided)              |
| **Tech Stack**      | Node.js 20+, Express.js 4.x, MongoDB 7, Mongoose ODM, Jest |
| **Difficulty**      | Intermediate                                              |
| **Prerequisites**   | Basic JavaScript/Node.js, REST concepts, MongoDB basics   |
| **Outcome**         | Participants build a fully functional product catalog API with search, inventory management, and analytics |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Functional Requirements](#2-functional-requirements)
   - [FR-1: Create Product](#fr-1-create-product)
   - [FR-2: List & Search Products](#fr-2-list--search-products)
   - [FR-3: Update Product](#fr-3-update-product)
   - [FR-4: Delete Product (Soft Delete)](#fr-4-delete-product-soft-delete)
   - [FR-5: Manage Inventory](#fr-5-manage-inventory)
   - [FR-6: Product Analytics](#fr-6-product-analytics)
3. [Non-Functional Requirements](#3-non-functional-requirements)
4. [Domain Model](#4-domain-model)
5. [API Contract](#5-api-contract)
6. [Data Model — Mongoose Schemas](#6-data-model--mongoose-schemas)
7. [Architecture](#7-architecture)
8. [Test Strategy](#8-test-strategy)
9. [Appendix](#9-appendix)

---

## 1. Introduction

### 1.1 Purpose

This document specifies the design for an **E-Commerce Product Catalog API** — a RESTful service that allows clients to create, search, update, and delete products. It also provides inventory management and basic product analytics. The exercise is designed for a **Faculty Development Program** to demonstrate AI-native software development practices.

### 1.2 Scope

The API covers the following capabilities:

- Full CRUD operations on products
- Full-text search with multi-field filtering and pagination
- Price history tracking on updates
- Soft-delete with restore capability
- Stock management with low-stock alerting
- Analytics endpoints (most viewed products, category breakdown)

### 1.3 Audience

Faculty members participating in the AI-Native Software Development workshop. Participants should be comfortable with JavaScript fundamentals and basic REST API concepts.

### 1.4 Conventions

| Convention        | Description                                      |
|-------------------|--------------------------------------------------|
| `kebab-case`      | URL path segments (`/api/products`)               |
| `camelCase`       | JSON field names (`imageUrl`, `priceHistory`)     |
| `PascalCase`      | Mongoose model names (`Product`, `Category`)      |
| ISO 8601          | All date/time fields (`2025-01-15T10:30:00.000Z`) |
| UUID / ObjectId   | MongoDB ObjectId for document identifiers         |

---

## 2. Functional Requirements

### FR-1: Create Product

| Field              | Detail                                           |
|--------------------|--------------------------------------------------|
| **ID**             | FR-1                                             |
| **Title**          | Create Product                                   |
| **Priority**       | P0 — Must Have                                   |
| **Actor**          | Admin / API Client                               |
| **HTTP Method**    | `POST`                                           |
| **Endpoint**       | `/api/products`                                  |
| **Estimated Time** | 15 minutes                                       |

#### Description

Create a new product in the catalog with all required and optional fields. The system must validate inputs, reject duplicates (by name within the same category), and return the newly created product with a generated ID.

#### Acceptance Criteria

1. **AC-1.1**: A `POST /api/products` request with a valid body returns `201 Created` with the full product object including a generated `_id` and timestamps.
2. **AC-1.2**: The `name` field is required, must be 3–200 characters, and is trimmed of leading/trailing whitespace.
3. **AC-1.3**: The `price` field is required and must be a positive number with at most 2 decimal places.
4. **AC-1.4**: The `category` field is required and must reference an existing category or be one of the pre-defined enum values.
5. **AC-1.5**: The `tags` field accepts an array of strings (max 10 tags, each 1–50 chars); duplicates within the array are silently removed.
6. **AC-1.6**: The `imageUrl` field, if provided, must be a valid URL (http or https scheme).
7. **AC-1.7**: The `stock` field defaults to `0` if not provided and must be a non-negative integer.

#### Edge Cases

1. **EC-1.1**: Submitting a product with a duplicate `name` + `category` combination returns `409 Conflict` with a descriptive error message.
2. **EC-1.2**: Sending an empty body or missing all required fields returns `400 Bad Request` with a validation errors array listing each missing field.
3. **EC-1.3**: Sending a `price` of `0` or a negative number returns `400 Bad Request` with message `"Price must be a positive number"`.
4. **EC-1.4**: Sending `tags` with more than 10 items returns `400 Bad Request`.
5. **EC-1.5**: Extremely long `description` (> 5000 chars) is rejected with `400 Bad Request`.

#### Request Body Example

```json
{
  "name": "Wireless Bluetooth Headphones",
  "description": "Premium noise-cancelling over-ear headphones with 30-hour battery life.",
  "price": 79.99,
  "category": "Electronics",
  "tags": ["wireless", "bluetooth", "noise-cancelling"],
  "imageUrl": "https://images.example.com/headphones-001.jpg",
  "stock": 150
}
```

#### Response Example — `201 Created`

```json
{
  "success": true,
  "data": {
    "_id": "665a1b2c3d4e5f6a7b8c9d0e",
    "name": "Wireless Bluetooth Headphones",
    "description": "Premium noise-cancelling over-ear headphones with 30-hour battery life.",
    "price": 79.99,
    "category": "Electronics",
    "tags": ["wireless", "bluetooth", "noise-cancelling"],
    "imageUrl": "https://images.example.com/headphones-001.jpg",
    "stock": 150,
    "viewCount": 0,
    "isDeleted": false,
    "createdAt": "2025-01-15T10:30:00.000Z",
    "updatedAt": "2025-01-15T10:30:00.000Z"
  }
}
```

---

### FR-2: List & Search Products

| Field              | Detail                                           |
|--------------------|--------------------------------------------------|
| **ID**             | FR-2                                             |
| **Title**          | List Products with Full-Text Search & Filtering  |
| **Priority**       | P0 — Must Have                                   |
| **Actor**          | Any API Client                                   |
| **HTTP Method**    | `GET`                                            |
| **Endpoint**       | `/api/products`                                  |
| **Estimated Time** | 20 minutes                                       |

#### Description

Retrieve a paginated list of products. Supports full-text search across `name` and `description`, filtering by `category`, price range (`minPrice`, `maxPrice`), and `tags`. Soft-deleted products are excluded by default.

#### Acceptance Criteria

1. **AC-2.1**: `GET /api/products` without parameters returns the first page of active (non-deleted) products with default pagination (`page=1`, `limit=10`).
2. **AC-2.2**: The `search` query parameter performs a MongoDB full-text search across `name` and `description` fields and returns results sorted by relevance score.
3. **AC-2.3**: The `category` query parameter filters products by exact category match (case-insensitive).
4. **AC-2.4**: The `minPrice` and `maxPrice` query parameters filter products within the specified price range (inclusive on both ends).
5. **AC-2.5**: The `tags` query parameter accepts a comma-separated list and returns products that contain **any** of the specified tags.
6. **AC-2.6**: The response includes pagination metadata: `totalCount`, `page`, `limit`, `totalPages`, `hasNextPage`, `hasPrevPage`.
7. **AC-2.7**: The `sortBy` parameter accepts `price`, `name`, `createdAt`, or `viewCount`; the `sortOrder` parameter accepts `asc` or `desc` (default: `createdAt` descending).

#### Edge Cases

1. **EC-2.1**: Searching with a term that matches no products returns `200 OK` with an empty `data` array and `totalCount: 0`.
2. **EC-2.2**: Providing `minPrice` greater than `maxPrice` returns `400 Bad Request` with message `"minPrice cannot exceed maxPrice"`.
3. **EC-2.3**: Requesting a `page` beyond the total pages returns `200 OK` with an empty `data` array.
4. **EC-2.4**: A `limit` exceeding 100 is clamped to 100; a `limit` less than 1 defaults to 10.
5. **EC-2.5**: Special characters in the `search` term are sanitized to prevent NoSQL injection.

#### Request Example

```
GET /api/products?search=headphones&category=Electronics&minPrice=50&maxPrice=200&tags=wireless,bluetooth&page=1&limit=10&sortBy=price&sortOrder=asc
```

#### Response Example — `200 OK`

```json
{
  "success": true,
  "data": [
    {
      "_id": "665a1b2c3d4e5f6a7b8c9d0e",
      "name": "Wireless Bluetooth Headphones",
      "description": "Premium noise-cancelling over-ear headphones...",
      "price": 79.99,
      "category": "Electronics",
      "tags": ["wireless", "bluetooth", "noise-cancelling"],
      "imageUrl": "https://images.example.com/headphones-001.jpg",
      "stock": 150,
      "viewCount": 42
    }
  ],
  "pagination": {
    "totalCount": 1,
    "page": 1,
    "limit": 10,
    "totalPages": 1,
    "hasNextPage": false,
    "hasPrevPage": false
  }
}
```

---

### FR-3: Update Product

| Field              | Detail                                           |
|--------------------|--------------------------------------------------|
| **ID**             | FR-3                                             |
| **Title**          | Update Product with Price History Tracking        |
| **Priority**       | P0 — Must Have                                   |
| **Actor**          | Admin / API Client                               |
| **HTTP Method**    | `PATCH`                                          |
| **Endpoint**       | `/api/products/:id`                              |
| **Estimated Time** | 20 minutes                                       |

#### Description

Update one or more fields of an existing product. Supports partial updates (only specified fields are changed). When the `price` field is modified, the system automatically records the old price in a price history collection for auditing and analytics.

#### Acceptance Criteria

1. **AC-3.1**: A `PATCH /api/products/:id` request with a valid partial body returns `200 OK` with the updated product.
2. **AC-3.2**: Only the fields present in the request body are updated; omitted fields remain unchanged.
3. **AC-3.3**: When `price` is updated, a new `PriceHistory` record is created with `{ productId, oldPrice, newPrice, changedAt }`.
4. **AC-3.4**: The `updatedAt` timestamp is automatically set to the current time on every update.
5. **AC-3.5**: Updating a soft-deleted product returns `404 Not Found` (deleted products cannot be updated).
6. **AC-3.6**: The `_id`, `createdAt`, and `isDeleted` fields cannot be modified via this endpoint; any attempt to set them is silently ignored.

#### Edge Cases

1. **EC-3.1**: Updating with an invalid ObjectId format for `:id` returns `400 Bad Request` with message `"Invalid product ID format"`.
2. **EC-3.2**: Updating with an empty body `{}` returns `200 OK` with the unchanged product (no-op).
3. **EC-3.3**: Setting `price` to the same value as the current price does **not** create a price history record (no actual change detected).
4. **EC-3.4**: Concurrent updates to the same product are handled via Mongoose versioning (`__v`) to prevent lost updates; a version conflict returns `409 Conflict`.

#### Request Example

```
PATCH /api/products/665a1b2c3d4e5f6a7b8c9d0e
Content-Type: application/json

{
  "price": 69.99,
  "stock": 120
}
```

#### Response Example — `200 OK`

```json
{
  "success": true,
  "data": {
    "_id": "665a1b2c3d4e5f6a7b8c9d0e",
    "name": "Wireless Bluetooth Headphones",
    "description": "Premium noise-cancelling over-ear headphones...",
    "price": 69.99,
    "category": "Electronics",
    "tags": ["wireless", "bluetooth", "noise-cancelling"],
    "imageUrl": "https://images.example.com/headphones-001.jpg",
    "stock": 120,
    "viewCount": 42,
    "isDeleted": false,
    "createdAt": "2025-01-15T10:30:00.000Z",
    "updatedAt": "2025-01-15T12:45:00.000Z"
  }
}
```

#### Price History Record Created

```json
{
  "_id": "665b2c3d4e5f6a7b8c9d0e1f",
  "productId": "665a1b2c3d4e5f6a7b8c9d0e",
  "oldPrice": 79.99,
  "newPrice": 69.99,
  "changedAt": "2025-01-15T12:45:00.000Z"
}
```

---

### FR-4: Delete Product (Soft Delete)

| Field              | Detail                                           |
|--------------------|--------------------------------------------------|
| **ID**             | FR-4                                             |
| **Title**          | Delete Product (Soft Delete)                     |
| **Priority**       | P0 — Must Have                                   |
| **Actor**          | Admin / API Client                               |
| **HTTP Method**    | `DELETE`                                         |
| **Endpoint**       | `/api/products/:id`                              |
| **Estimated Time** | 10 minutes                                       |

#### Description

Soft-delete a product by setting its `isDeleted` flag to `true` and recording a `deletedAt` timestamp. The product remains in the database but is excluded from all listing and search queries. An additional restore endpoint allows un-deleting a product.

#### Acceptance Criteria

1. **AC-4.1**: A `DELETE /api/products/:id` request sets `isDeleted: true` and `deletedAt: <current timestamp>` and returns `200 OK` with the message `"Product deleted successfully"`.
2. **AC-4.2**: After soft-deletion, the product no longer appears in `GET /api/products` results.
3. **AC-4.3**: A `GET /api/products/:id` request for a soft-deleted product returns `404 Not Found`.
4. **AC-4.4**: A `PATCH /api/products/:id/restore` request sets `isDeleted: false` and `deletedAt: null` and returns `200 OK` with the restored product.
5. **AC-4.5**: Deleting an already-deleted product returns `404 Not Found`.

#### Edge Cases

1. **EC-4.1**: Attempting to delete a product with an invalid ObjectId returns `400 Bad Request`.
2. **EC-4.2**: Attempting to restore a product that is not deleted returns `400 Bad Request` with message `"Product is not deleted"`.
3. **EC-4.3**: Restoring a product that does not exist at all returns `404 Not Found`.

#### Response Example — `200 OK` (Delete)

```json
{
  "success": true,
  "message": "Product deleted successfully",
  "data": {
    "_id": "665a1b2c3d4e5f6a7b8c9d0e",
    "isDeleted": true,
    "deletedAt": "2025-01-15T14:00:00.000Z"
  }
}
```

#### Response Example — `200 OK` (Restore)

```json
{
  "success": true,
  "message": "Product restored successfully",
  "data": {
    "_id": "665a1b2c3d4e5f6a7b8c9d0e",
    "name": "Wireless Bluetooth Headphones",
    "price": 69.99,
    "isDeleted": false,
    "deletedAt": null
  }
}
```

---

### FR-5: Manage Inventory

| Field              | Detail                                           |
|--------------------|--------------------------------------------------|
| **ID**             | FR-5                                             |
| **Title**          | Manage Inventory (Stock Increment/Decrement & Low Stock Alerts) |
| **Priority**       | P1 — Should Have                                 |
| **Actor**          | Admin / API Client                               |
| **HTTP Methods**   | `PATCH`, `GET`                                   |
| **Endpoints**      | `PATCH /api/products/:id/stock`, `GET /api/products/low-stock` |
| **Estimated Time** | 15 minutes                                       |

#### Description

Manage product inventory by incrementing or decrementing stock levels. When stock falls below a configurable threshold (default: 10), a `StockAlert` record is created. A dedicated endpoint lists all products currently below the low-stock threshold.

#### Acceptance Criteria

1. **AC-5.1**: A `PATCH /api/products/:id/stock` request with `{ "action": "increment", "quantity": 50 }` increases the product stock by 50 and returns the updated product.
2. **AC-5.2**: A `PATCH /api/products/:id/stock` request with `{ "action": "decrement", "quantity": 10 }` decreases the product stock by 10 and returns the updated product.
3. **AC-5.3**: When stock falls to or below the low-stock threshold (default: 10), a `StockAlert` document is created with `{ productId, currentStock, threshold, alertedAt }`.
4. **AC-5.4**: `GET /api/products/low-stock` returns all products with `stock <= threshold`, sorted by stock ascending.
5. **AC-5.5**: The low-stock threshold is configurable via the `LOW_STOCK_THRESHOLD` environment variable.
6. **AC-5.6**: Stock operations use MongoDB's `$inc` operator for atomic updates to prevent race conditions.

#### Edge Cases

1. **EC-5.1**: Decrementing stock below 0 returns `400 Bad Request` with message `"Insufficient stock. Current stock: <n>"`.
2. **EC-5.2**: Sending a non-positive `quantity` (0 or negative) returns `400 Bad Request`.
3. **EC-5.3**: Sending an invalid `action` (not `increment` or `decrement`) returns `400 Bad Request` with message `"Action must be 'increment' or 'decrement'"`.
4. **EC-5.4**: Duplicate `StockAlert` records are prevented — only one alert per product is active at a time. Re-entering low stock after a restock creates a new alert only if the previous one was resolved.

#### Request Example — Stock Decrement

```
PATCH /api/products/665a1b2c3d4e5f6a7b8c9d0e/stock
Content-Type: application/json

{
  "action": "decrement",
  "quantity": 145
}
```

#### Response Example — `200 OK`

```json
{
  "success": true,
  "data": {
    "_id": "665a1b2c3d4e5f6a7b8c9d0e",
    "name": "Wireless Bluetooth Headphones",
    "stock": 5,
    "lowStockAlert": {
      "triggered": true,
      "threshold": 10,
      "alertedAt": "2025-01-15T15:30:00.000Z"
    }
  }
}
```

#### Response Example — `GET /api/products/low-stock`

```json
{
  "success": true,
  "data": [
    {
      "_id": "665a1b2c3d4e5f6a7b8c9d0e",
      "name": "Wireless Bluetooth Headphones",
      "stock": 5,
      "category": "Electronics",
      "threshold": 10
    },
    {
      "_id": "665c3d4e5f6a7b8c9d0e1f2a",
      "name": "USB-C Charging Cable",
      "stock": 3,
      "category": "Accessories",
      "threshold": 10
    }
  ],
  "count": 2
}
```

---

### FR-6: Product Analytics

| Field              | Detail                                           |
|--------------------|--------------------------------------------------|
| **ID**             | FR-6                                             |
| **Title**          | Product Analytics (Most Viewed & Category Breakdown) |
| **Priority**       | P2 — Nice to Have                                |
| **Actor**          | Admin / API Client                               |
| **HTTP Method**    | `GET`                                            |
| **Endpoints**      | `GET /api/analytics/top-products`, `GET /api/analytics/categories` |
| **Estimated Time** | 15 minutes                                       |

#### Description

Provide analytics endpoints that return the most-viewed products and a category-level breakdown of product counts, average prices, and total stock. Each time a product is retrieved by ID (`GET /api/products/:id`), its `viewCount` is incremented.

#### Acceptance Criteria

1. **AC-6.1**: `GET /api/products/:id` increments the product's `viewCount` by 1 on each successful retrieval.
2. **AC-6.2**: `GET /api/analytics/top-products?limit=10` returns the top N products sorted by `viewCount` descending (default `limit=10`, max `limit=50`).
3. **AC-6.3**: `GET /api/analytics/categories` returns an aggregation of all categories with `productCount`, `averagePrice`, `totalStock`, `minPrice`, and `maxPrice` for each category.
4. **AC-6.4**: Analytics endpoints exclude soft-deleted products.
5. **AC-6.5**: The category breakdown is computed using MongoDB's aggregation pipeline (`$group`, `$match`, `$sort`).

#### Edge Cases

1. **EC-6.1**: When no products exist, `GET /api/analytics/top-products` returns `200 OK` with an empty array.
2. **EC-6.2**: When `limit` is not a valid positive integer, it defaults to 10.
3. **EC-6.3**: Categories with all products soft-deleted do not appear in the category breakdown.

#### Response Example — `GET /api/analytics/top-products?limit=3`

```json
{
  "success": true,
  "data": [
    {
      "_id": "665a1b2c3d4e5f6a7b8c9d0e",
      "name": "Wireless Bluetooth Headphones",
      "category": "Electronics",
      "price": 69.99,
      "viewCount": 342
    },
    {
      "_id": "665d4e5f6a7b8c9d0e1f2a3b",
      "name": "Organic Green Tea (50 bags)",
      "category": "Groceries",
      "price": 12.49,
      "viewCount": 287
    },
    {
      "_id": "665e5f6a7b8c9d0e1f2a3b4c",
      "name": "Running Shoes — Ultralight",
      "category": "Sports",
      "price": 129.00,
      "viewCount": 215
    }
  ]
}
```

#### Response Example — `GET /api/analytics/categories`

```json
{
  "success": true,
  "data": [
    {
      "category": "Electronics",
      "productCount": 45,
      "averagePrice": 149.95,
      "totalStock": 2340,
      "minPrice": 9.99,
      "maxPrice": 999.99
    },
    {
      "category": "Groceries",
      "productCount": 120,
      "averagePrice": 8.75,
      "totalStock": 15600,
      "minPrice": 0.99,
      "maxPrice": 49.99
    },
    {
      "category": "Sports",
      "productCount": 32,
      "averagePrice": 89.50,
      "totalStock": 890,
      "minPrice": 14.99,
      "maxPrice": 499.99
    }
  ]
}
```

---

## 3. Non-Functional Requirements

### NFR-1: Response Time

| Metric                    | Target            |
|---------------------------|-------------------|
| Simple CRUD operations    | ≤ 200 ms (p95)   |
| Full-text search          | ≤ 500 ms (p95)   |
| Analytics aggregation     | ≤ 1 000 ms (p95) |
| Health check              | ≤ 50 ms (p95)    |

### NFR-2: Concurrent Users

| Metric                      | Target              |
|-----------------------------|---------------------|
| Concurrent API connections  | 100 simultaneous    |
| Requests per second         | 500 RPS sustained   |
| Connection pool size        | 10 MongoDB connections |

### NFR-3: Data Volume

| Metric                      | Target              |
|-----------------------------|---------------------|
| Products in catalog         | Up to 100,000       |
| Price history records       | Up to 1,000,000     |
| Search index size           | ≤ 500 MB            |
| Average document size       | ≤ 2 KB              |

### NFR-4: Reliability & Error Handling

| Requirement                  | Detail                                        |
|------------------------------|-----------------------------------------------|
| Error response format        | Consistent JSON: `{ success: false, error: { code, message, details } }` |
| Input validation             | All inputs validated before DB operations     |
| Graceful MongoDB disconnects | Automatic reconnection with exponential backoff |
| Request timeout              | 30 seconds max per request                    |

### NFR-5: Security

| Requirement            | Detail                                         |
|------------------------|-------------------------------------------------|
| Input sanitization     | Prevent NoSQL injection via `mongo-sanitize`    |
| Rate limiting          | 100 requests/min per IP via `express-rate-limit` |
| CORS                   | Configurable allowed origins                    |
| Helmet.js              | Security headers enabled                        |

---

## 4. Domain Model

### 4.1 Entity Relationship Overview

```
┌──────────────┐       1..* ┌──────────────────┐
│   Product    │───────────▶│   PriceHistory   │
│              │            │                  │
│  _id         │            │  _id             │
│  name        │            │  productId (FK)  │
│  description │            │  oldPrice        │
│  price       │            │  newPrice        │
│  category    │            │  changedAt       │
│  tags[]      │            └──────────────────┘
│  imageUrl    │
│  stock       │       0..* ┌──────────────────┐
│  viewCount   │───────────▶│   StockAlert     │
│  isDeleted   │            │                  │
│  deletedAt   │            │  _id             │
│  createdAt   │            │  productId (FK)  │
│  updatedAt   │            │  currentStock    │
└──────┬───────┘            │  threshold       │
       │                    │  resolved        │
       │ belongs to         │  alertedAt       │
       ▼                    │  resolvedAt      │
┌──────────────┐            └──────────────────┘
│   Category   │
│              │
│  _id         │
│  name        │
│  slug        │
│  description │
│  productCount│
│  createdAt   │
└──────────────┘
```

### 4.2 Entity Descriptions

| Entity         | Description                                                       |
|----------------|-------------------------------------------------------------------|
| **Product**    | Core catalog item with pricing, stock, and metadata               |
| **Category**   | Classification group for products (e.g., Electronics, Groceries)  |
| **PriceHistory** | Immutable audit log of price changes for a product             |
| **StockAlert** | Alert record created when stock drops below threshold             |

---

## 5. API Contract

### 5.1 Base URL

```
http://localhost:3000/api
```

### 5.2 Common Response Envelope

All responses follow a consistent envelope:

```json
{
  "success": true | false,
  "data": { ... } | [ ... ],
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable message",
    "details": [ ... ]
  },
  "pagination": { ... }
}
```

### 5.3 Endpoints Summary

| Method   | Endpoint                          | Description                       | Auth  |
|----------|-----------------------------------|-----------------------------------|-------|
| `POST`   | `/api/products`                   | Create a new product              | None  |
| `GET`    | `/api/products`                   | List/search products              | None  |
| `GET`    | `/api/products/:id`               | Get product by ID (increments view) | None |
| `PATCH`  | `/api/products/:id`               | Update product (partial)          | None  |
| `DELETE` | `/api/products/:id`               | Soft-delete product               | None  |
| `PATCH`  | `/api/products/:id/restore`       | Restore soft-deleted product      | None  |
| `PATCH`  | `/api/products/:id/stock`         | Increment/decrement stock         | None  |
| `GET`    | `/api/products/low-stock`         | List low-stock products           | None  |
| `GET`    | `/api/analytics/top-products`     | Most viewed products              | None  |
| `GET`    | `/api/analytics/categories`       | Category breakdown                | None  |
| `GET`    | `/api/health`                     | Health check                      | None  |

### 5.4 Error Codes

| HTTP Status | Error Code            | Description                           |
|-------------|-----------------------|---------------------------------------|
| 400         | `VALIDATION_ERROR`    | Request body failed validation        |
| 400         | `INVALID_ID`          | The provided ID is not a valid ObjectId |
| 404         | `NOT_FOUND`           | Resource not found or soft-deleted    |
| 409         | `DUPLICATE_PRODUCT`   | Product with same name+category exists |
| 409         | `VERSION_CONFLICT`    | Concurrent modification detected      |
| 422         | `INSUFFICIENT_STOCK`  | Not enough stock for decrement        |
| 429         | `RATE_LIMIT_EXCEEDED` | Too many requests                     |
| 500         | `INTERNAL_ERROR`      | Unexpected server error               |

### 5.5 Detailed Error Response Example

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "price",
        "message": "Price must be a positive number",
        "received": -5
      },
      {
        "field": "name",
        "message": "Name is required"
      }
    ]
  }
}
```

### 5.6 Health Check — `GET /api/health`

#### Response Example — `200 OK`

```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "timestamp": "2025-01-15T10:00:00.000Z",
    "uptime": 3600,
    "mongodb": "connected",
    "version": "1.0.0"
  }
}
```

---

## 6. Data Model — Mongoose Schemas

### 6.1 Product Schema

```javascript
// models/Product.js
const mongoose = require('mongoose');

const productSchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: [true, 'Product name is required'],
      trim: true,
      minlength: [3, 'Name must be at least 3 characters'],
      maxlength: [200, 'Name cannot exceed 200 characters'],
    },
    description: {
      type: String,
      trim: true,
      maxlength: [5000, 'Description cannot exceed 5000 characters'],
      default: '',
    },
    price: {
      type: Number,
      required: [true, 'Price is required'],
      min: [0.01, 'Price must be a positive number'],
    },
    category: {
      type: String,
      required: [true, 'Category is required'],
      enum: {
        values: [
          'Electronics',
          'Clothing',
          'Groceries',
          'Sports',
          'Books',
          'Home',
          'Toys',
          'Accessories',
        ],
        message: '{VALUE} is not a valid category',
      },
    },
    tags: {
      type: [String],
      validate: {
        validator: function (v) {
          return v.length <= 10;
        },
        message: 'A product can have at most 10 tags',
      },
      default: [],
    },
    imageUrl: {
      type: String,
      validate: {
        validator: function (v) {
          if (!v) return true;
          return /^https?:\/\/.+/.test(v);
        },
        message: 'Image URL must be a valid HTTP/HTTPS URL',
      },
    },
    stock: {
      type: Number,
      default: 0,
      min: [0, 'Stock cannot be negative'],
      validate: {
        validator: Number.isInteger,
        message: 'Stock must be an integer',
      },
    },
    viewCount: {
      type: Number,
      default: 0,
      min: 0,
    },
    isDeleted: {
      type: Boolean,
      default: false,
    },
    deletedAt: {
      type: Date,
      default: null,
    },
  },
  {
    timestamps: true,
    versionKey: '__v',
  }
);

// ── Indexes ───────────────────────────────────────────────
productSchema.index({ name: 'text', description: 'text' });
productSchema.index({ category: 1, isDeleted: 1 });
productSchema.index({ price: 1 });
productSchema.index({ tags: 1 });
productSchema.index({ viewCount: -1 });
productSchema.index({ name: 1, category: 1 }, { unique: true });
productSchema.index({ stock: 1, isDeleted: 1 });

// ── Pre-save: deduplicate tags ────────────────────────────
productSchema.pre('save', function (next) {
  if (this.tags && this.tags.length) {
    this.tags = [...new Set(this.tags.map((t) => t.trim().toLowerCase()))];
  }
  next();
});

module.exports = mongoose.model('Product', productSchema);
```

### 6.2 Category Schema

```javascript
// models/Category.js
const mongoose = require('mongoose');

const categorySchema = new mongoose.Schema(
  {
    name: {
      type: String,
      required: true,
      unique: true,
      trim: true,
    },
    slug: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
    },
    description: {
      type: String,
      default: '',
    },
    productCount: {
      type: Number,
      default: 0,
      min: 0,
    },
  },
  {
    timestamps: true,
  }
);

// ── Indexes ───────────────────────────────────────────────
categorySchema.index({ slug: 1 });
categorySchema.index({ name: 1 });

module.exports = mongoose.model('Category', categorySchema);
```

### 6.3 PriceHistory Schema

```javascript
// models/PriceHistory.js
const mongoose = require('mongoose');

const priceHistorySchema = new mongoose.Schema({
  productId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Product',
    required: true,
    index: true,
  },
  oldPrice: {
    type: Number,
    required: true,
  },
  newPrice: {
    type: Number,
    required: true,
  },
  changedAt: {
    type: Date,
    default: Date.now,
  },
});

// ── Indexes ───────────────────────────────────────────────
priceHistorySchema.index({ productId: 1, changedAt: -1 });

module.exports = mongoose.model('PriceHistory', priceHistorySchema);
```

### 6.4 StockAlert Schema

```javascript
// models/StockAlert.js
const mongoose = require('mongoose');

const stockAlertSchema = new mongoose.Schema({
  productId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Product',
    required: true,
  },
  currentStock: {
    type: Number,
    required: true,
  },
  threshold: {
    type: Number,
    required: true,
  },
  resolved: {
    type: Boolean,
    default: false,
  },
  alertedAt: {
    type: Date,
    default: Date.now,
  },
  resolvedAt: {
    type: Date,
    default: null,
  },
});

// ── Indexes ───────────────────────────────────────────────
stockAlertSchema.index({ productId: 1, resolved: 1 });
stockAlertSchema.index({ alertedAt: -1 });

module.exports = mongoose.model('StockAlert', stockAlertSchema);
```

---

## 7. Architecture

### 7.1 Layered Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Client (HTTP)                       │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│  Routes Layer                                           │
│  ┌─────────────────┐ ┌──────────────────┐               │
│  │ productRoutes.js│ │ analyticsRoutes.js│               │
│  └────────┬────────┘ └────────┬─────────┘               │
└───────────┼───────────────────┼─────────────────────────┘
            │                   │
┌───────────▼───────────────────▼─────────────────────────┐
│  Controllers Layer                                      │
│  ┌─────────────────────┐ ┌────────────────────────┐     │
│  │ productController.js│ │ analyticsController.js  │     │
│  └────────┬────────────┘ └────────┬───────────────┘     │
└───────────┼───────────────────────┼─────────────────────┘
            │                       │
┌───────────▼───────────────────────▼─────────────────────┐
│  Services Layer (Business Logic)                        │
│  ┌──────────────────┐ ┌──────────────────────────┐      │
│  │ productService.js│ │ analyticsService.js       │      │
│  └────────┬─────────┘ └────────┬─────────────────┘      │
└───────────┼────────────────────┼────────────────────────┘
            │                    │
┌───────────▼────────────────────▼────────────────────────┐
│  Models Layer (Mongoose Schemas)                        │
│  ┌──────────┐ ┌──────────┐ ┌─────────────┐ ┌────────┐  │
│  │ Product  │ │ Category │ │ PriceHistory│ │StockAlert│ │
│  └──────────┘ └──────────┘ └─────────────┘ └────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                   MongoDB 7                             │
└─────────────────────────────────────────────────────────┘
```

### 7.2 Project Structure

```
ecommerce-product-catalog/
├── src/
│   ├── app.js                    # Express app setup, middleware
│   ├── server.js                 # HTTP server entry point
│   ├── config/
│   │   └── db.js                 # MongoDB connection config
│   ├── routes/
│   │   ├── productRoutes.js      # Product CRUD + stock routes
│   │   └── analyticsRoutes.js    # Analytics routes
│   ├── controllers/
│   │   ├── productController.js  # Request/response handling
│   │   └── analyticsController.js
│   ├── services/
│   │   ├── productService.js     # Business logic
│   │   └── analyticsService.js
│   ├── models/
│   │   ├── Product.js
│   │   ├── Category.js
│   │   ├── PriceHistory.js
│   │   └── StockAlert.js
│   ├── middleware/
│   │   ├── errorHandler.js       # Global error handler
│   │   ├── validateObjectId.js   # ObjectId format validator
│   │   └── rateLimiter.js        # Rate limiting middleware
│   └── utils/
│       ├── ApiError.js           # Custom error class
│       └── sanitize.js           # Input sanitization
├── tests/
│   ├── unit/
│   │   ├── productService.test.js
│   │   └── analyticsService.test.js
│   ├── integration/
│   │   ├── product.api.test.js
│   │   └── analytics.api.test.js
│   └── setup.js                  # Jest global setup (MongoDB Memory Server)
├── .env
├── .env.example
├── docker-compose.yml
├── package.json
├── jest.config.js
└── README.md
```

### 7.3 Middleware Pipeline

```
Request
  │
  ▼
express.json()          ──▶  Parse JSON body
  │
  ▼
helmet()                ──▶  Security headers
  │
  ▼
cors()                  ──▶  CORS headers
  │
  ▼
rateLimiter()           ──▶  Rate limiting (100 req/min)
  │
  ▼
morgan('dev')           ──▶  Request logging
  │
  ▼
Route Handler           ──▶  Controller → Service → Model
  │
  ▼
errorHandler()          ──▶  Global error handler
  │
  ▼
Response
```

### 7.4 Key Design Decisions

| Decision                  | Rationale                                                  |
|---------------------------|------------------------------------------------------------|
| Soft delete over hard delete | Preserves data for analytics and allows undo             |
| Price history as separate collection | Keeps Product documents lean; history can grow large |
| MongoDB text index for search | Native full-text search, no extra infrastructure needed |
| Layered architecture      | Clear separation of concerns; testable service layer       |
| Mongoose ODM              | Schema validation, middleware hooks, population support    |
| Atomic `$inc` for stock   | Prevents race conditions on concurrent stock changes       |

---

## 8. Test Strategy

### 8.1 Testing Pyramid

| Layer          | Tool                        | Count (min) | Focus                               |
|----------------|-----------------------------|-------------|--------------------------------------|
| Unit Tests     | Jest                        | 15+         | Service layer logic, validation      |
| Integration    | Jest + Supertest            | 12+         | Full HTTP request/response cycles    |
| DB Tests       | MongoDB Memory Server       | —           | In-memory MongoDB for test isolation |

### 8.2 Unit Test Examples

```javascript
// tests/unit/productService.test.js
const productService = require('../../src/services/productService');

describe('ProductService', () => {
  describe('createProduct', () => {
    it('should create a product with valid data', async () => {
      const productData = {
        name: 'Test Product',
        price: 29.99,
        category: 'Electronics',
        stock: 100,
      };
      const result = await productService.createProduct(productData);

      expect(result).toHaveProperty('_id');
      expect(result.name).toBe('Test Product');
      expect(result.price).toBe(29.99);
      expect(result.isDeleted).toBe(false);
      expect(result.viewCount).toBe(0);
    });

    it('should reject a product with negative price', async () => {
      const productData = { name: 'Bad Product', price: -10, category: 'Books' };
      await expect(productService.createProduct(productData))
        .rejects.toThrow('Price must be a positive number');
    });

    it('should deduplicate tags', async () => {
      const productData = {
        name: 'Tagged Product',
        price: 10.00,
        category: 'Books',
        tags: ['fiction', 'Fiction', 'FICTION', 'novel'],
      };
      const result = await productService.createProduct(productData);
      expect(result.tags).toEqual(['fiction', 'novel']);
    });
  });

  describe('updateProduct', () => {
    it('should create price history when price changes', async () => {
      // ... setup and assertions
    });

    it('should not create price history when price unchanged', async () => {
      // ... setup and assertions
    });
  });

  describe('manageStock', () => {
    it('should reject decrement below zero', async () => {
      // ... setup and assertions
    });

    it('should create stock alert when below threshold', async () => {
      // ... setup and assertions
    });
  });
});
```

### 8.3 Integration Test Examples

```javascript
// tests/integration/product.api.test.js
const request = require('supertest');
const app = require('../../src/app');

describe('Product API', () => {
  describe('POST /api/products', () => {
    it('should return 201 for valid product', async () => {
      const res = await request(app)
        .post('/api/products')
        .send({
          name: 'Integration Test Product',
          price: 49.99,
          category: 'Electronics',
          stock: 50,
        });

      expect(res.status).toBe(201);
      expect(res.body.success).toBe(true);
      expect(res.body.data).toHaveProperty('_id');
    });

    it('should return 400 for missing required fields', async () => {
      const res = await request(app)
        .post('/api/products')
        .send({});

      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
      expect(res.body.error.code).toBe('VALIDATION_ERROR');
    });

    it('should return 409 for duplicate name+category', async () => {
      const product = {
        name: 'Duplicate Product',
        price: 10.00,
        category: 'Books',
      };
      await request(app).post('/api/products').send(product);
      const res = await request(app).post('/api/products').send(product);

      expect(res.status).toBe(409);
      expect(res.body.error.code).toBe('DUPLICATE_PRODUCT');
    });
  });

  describe('GET /api/products', () => {
    it('should return paginated products', async () => {
      const res = await request(app)
        .get('/api/products')
        .query({ page: 1, limit: 5 });

      expect(res.status).toBe(200);
      expect(res.body).toHaveProperty('pagination');
      expect(res.body.pagination.limit).toBe(5);
    });

    it('should filter by category', async () => {
      const res = await request(app)
        .get('/api/products')
        .query({ category: 'Electronics' });

      expect(res.status).toBe(200);
      res.body.data.forEach((product) => {
        expect(product.category).toBe('Electronics');
      });
    });

    it('should filter by price range', async () => {
      const res = await request(app)
        .get('/api/products')
        .query({ minPrice: 10, maxPrice: 50 });

      expect(res.status).toBe(200);
      res.body.data.forEach((product) => {
        expect(product.price).toBeGreaterThanOrEqual(10);
        expect(product.price).toBeLessThanOrEqual(50);
      });
    });
  });

  describe('DELETE /api/products/:id', () => {
    it('should soft-delete a product', async () => {
      // Create then delete
      const createRes = await request(app)
        .post('/api/products')
        .send({ name: 'To Delete', price: 5.00, category: 'Books' });
      const id = createRes.body.data._id;

      const deleteRes = await request(app).delete(`/api/products/${id}`);
      expect(deleteRes.status).toBe(200);
      expect(deleteRes.body.data.isDeleted).toBe(true);

      // Verify it's hidden from listings
      const getRes = await request(app).get(`/api/products/${id}`);
      expect(getRes.status).toBe(404);
    });
  });
});
```

### 8.4 Test Configuration

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'node',
  testMatch: ['**/tests/**/*.test.js'],
  setupFilesAfterSetup: ['./tests/setup.js'],
  coverageDirectory: 'coverage',
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  testTimeout: 10000,
};
```

```javascript
// tests/setup.js
const { MongoMemoryServer } = require('mongodb-memory-server');
const mongoose = require('mongoose');

let mongoServer;

beforeAll(async () => {
  mongoServer = await MongoMemoryServer.create();
  const uri = mongoServer.getUri();
  await mongoose.connect(uri);
});

afterAll(async () => {
  await mongoose.disconnect();
  await mongoServer.stop();
});

afterEach(async () => {
  const collections = mongoose.connection.collections;
  for (const key in collections) {
    await collections[key].deleteMany({});
  }
});
```

---

## 9. Appendix

### A. Docker Compose — MongoDB Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  mongodb:
    image: mongo:7
    container_name: product-catalog-mongo
    ports:
      - '27017:27017'
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password123
      MONGO_INITDB_DATABASE: product_catalog
    volumes:
      - mongo_data:/data/db
      - ./scripts/mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js:ro
    restart: unless-stopped

  mongo-express:
    image: mongo-express:latest
    container_name: product-catalog-mongo-ui
    ports:
      - '8081:8081'
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: admin
      ME_CONFIG_MONGODB_ADMINPASSWORD: password123
      ME_CONFIG_MONGODB_URL: mongodb://admin:password123@mongodb:27017/
    depends_on:
      - mongodb
    restart: unless-stopped

volumes:
  mongo_data:
```

### B. Environment Configuration

```bash
# .env.example
# ── Server ─────────────────────────────────────────
PORT=3000
NODE_ENV=development

# ── MongoDB ────────────────────────────────────────
MONGODB_URI=mongodb://admin:password123@localhost:27017/product_catalog?authSource=admin

# ── Application ────────────────────────────────────
LOW_STOCK_THRESHOLD=10
DEFAULT_PAGE_SIZE=10
MAX_PAGE_SIZE=100

# ── Rate Limiting ──────────────────────────────────
RATE_LIMIT_WINDOW_MS=60000
RATE_LIMIT_MAX_REQUESTS=100
```

### C. Package Configuration

```json
{
  "name": "ecommerce-product-catalog",
  "version": "1.0.0",
  "description": "E-Commerce Product Catalog API — Faculty Development Program",
  "main": "src/server.js",
  "scripts": {
    "start": "node src/server.js",
    "dev": "nodemon src/server.js",
    "test": "jest --runInBand --forceExit",
    "test:watch": "jest --watch --runInBand",
    "test:coverage": "jest --coverage --runInBand --forceExit",
    "lint": "eslint src/ tests/",
    "seed": "node scripts/seed.js"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "dotenv": "^16.4.5",
    "express": "^4.21.0",
    "express-rate-limit": "^7.4.0",
    "helmet": "^7.1.0",
    "mongoose": "^8.6.0",
    "mongo-sanitize": "^1.1.0",
    "morgan": "^1.10.0"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "mongodb-memory-server": "^10.0.0",
    "nodemon": "^3.1.4",
    "supertest": "^7.0.0",
    "eslint": "^9.9.0"
  }
}
```

### D. MongoDB Initialization Script

```javascript
// scripts/mongo-init.js
db = db.getSiblingDB('product_catalog');

db.createCollection('products');
db.createCollection('pricehistories');
db.createCollection('stockalerts');

// Create text index for search
db.products.createIndex(
  { name: 'text', description: 'text' },
  { weights: { name: 10, description: 5 }, name: 'product_text_search' }
);

// Create compound indexes
db.products.createIndex({ category: 1, isDeleted: 1 });
db.products.createIndex({ price: 1 });
db.products.createIndex({ tags: 1 });
db.products.createIndex({ viewCount: -1 });
db.products.createIndex({ name: 1, category: 1 }, { unique: true });
db.products.createIndex({ stock: 1, isDeleted: 1 });

db.pricehistories.createIndex({ productId: 1, changedAt: -1 });
db.stockalerts.createIndex({ productId: 1, resolved: 1 });

print('Database initialized with indexes.');
```

### E. Sample Seed Data

```javascript
// scripts/seed.js
require('dotenv').config();
const mongoose = require('mongoose');
const Product = require('../src/models/Product');

const sampleProducts = [
  {
    name: 'Wireless Bluetooth Headphones',
    description: 'Premium noise-cancelling over-ear headphones with 30-hour battery life and comfortable memory foam ear cups.',
    price: 79.99,
    category: 'Electronics',
    tags: ['wireless', 'bluetooth', 'noise-cancelling', 'audio'],
    imageUrl: 'https://images.example.com/headphones-001.jpg',
    stock: 150,
  },
  {
    name: 'Organic Green Tea — 50 bags',
    description: 'Certified organic Japanese green tea. Rich in antioxidants with a smooth, mellow flavor.',
    price: 12.49,
    category: 'Groceries',
    tags: ['organic', 'tea', 'japanese', 'healthy'],
    imageUrl: 'https://images.example.com/green-tea-001.jpg',
    stock: 500,
  },
  {
    name: 'Running Shoes — Ultralight',
    description: 'Lightweight running shoes with responsive cushioning and breathable mesh upper. Ideal for marathon training.',
    price: 129.00,
    category: 'Sports',
    tags: ['running', 'lightweight', 'marathon', 'shoes'],
    imageUrl: 'https://images.example.com/running-shoes-001.jpg',
    stock: 75,
  },
  {
    name: 'USB-C Charging Cable (2m)',
    description: 'Braided nylon USB-C to USB-C cable with 100W power delivery support. Compatible with laptops, tablets, and phones.',
    price: 14.99,
    category: 'Accessories',
    tags: ['usb-c', 'charging', 'cable', 'fast-charging'],
    imageUrl: 'https://images.example.com/usbc-cable-001.jpg',
    stock: 1000,
  },
  {
    name: 'JavaScript: The Good Parts',
    description: 'Classic programming book by Douglas Crockford. A must-read for every JavaScript developer.',
    price: 24.99,
    category: 'Books',
    tags: ['javascript', 'programming', 'classic', 'learning'],
    imageUrl: 'https://images.example.com/js-good-parts-001.jpg',
    stock: 200,
  },
  {
    name: 'Stainless Steel Water Bottle (750ml)',
    description: 'Double-walled vacuum insulated water bottle. Keeps drinks cold for 24 hours or hot for 12 hours.',
    price: 19.99,
    category: 'Home',
    tags: ['water-bottle', 'insulated', 'eco-friendly', 'stainless-steel'],
    imageUrl: 'https://images.example.com/water-bottle-001.jpg',
    stock: 300,
  },
  {
    name: 'Wooden Building Blocks (100 pcs)',
    description: 'Natural wood building blocks in various shapes and colors. Non-toxic, child-safe finish. Ages 3+.',
    price: 34.99,
    category: 'Toys',
    tags: ['building', 'wooden', 'educational', 'kids'],
    imageUrl: 'https://images.example.com/blocks-001.jpg',
    stock: 80,
  },
  {
    name: 'Slim Fit Cotton T-Shirt',
    description: '100% combed cotton crew-neck t-shirt. Pre-shrunk, tagless comfort. Available in multiple colors.',
    price: 18.50,
    category: 'Clothing',
    tags: ['cotton', 't-shirt', 'slim-fit', 'basics'],
    imageUrl: 'https://images.example.com/tshirt-001.jpg',
    stock: 450,
  },
  {
    name: 'Portable Bluetooth Speaker',
    description: 'Waterproof portable speaker with 360° sound and 12-hour battery life. Perfect for outdoor adventures.',
    price: 49.99,
    category: 'Electronics',
    tags: ['speaker', 'bluetooth', 'waterproof', 'portable'],
    imageUrl: 'https://images.example.com/speaker-001.jpg',
    stock: 8,
  },
  {
    name: 'Yoga Mat — Premium Non-Slip',
    description: 'Extra thick 6mm yoga mat with alignment lines. Non-slip surface on both sides. Includes carry strap.',
    price: 39.99,
    category: 'Sports',
    tags: ['yoga', 'mat', 'non-slip', 'fitness'],
    imageUrl: 'https://images.example.com/yoga-mat-001.jpg',
    stock: 120,
  },
];

async function seed() {
  try {
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('Connected to MongoDB');

    await Product.deleteMany({});
    console.log('Cleared existing products');

    const created = await Product.insertMany(sampleProducts);
    console.log(`Seeded ${created.length} products`);

    await mongoose.disconnect();
    console.log('Done!');
  } catch (error) {
    console.error('Seed failed:', error);
    process.exit(1);
  }
}

seed();
```

### F. Quick Start Guide

```bash
# 1. Clone and install
git clone <repository-url>
cd ecommerce-product-catalog
npm install

# 2. Start MongoDB (via Docker)
docker-compose up -d

# 3. Configure environment
cp .env.example .env

# 4. Seed sample data
npm run seed

# 5. Start development server
npm run dev

# 6. Test the API
curl http://localhost:3000/api/health

# 7. Run tests
npm test

# 8. Run tests with coverage
npm run test:coverage
```

### G. Workshop Timeline

| Time          | Activity                                      | FR Covered |
|---------------|-----------------------------------------------|------------|
| 0:00 – 0:10  | Project setup, Docker Compose, `npm install`  | —          |
| 0:10 – 0:25  | Implement Create Product (model + route)      | FR-1       |
| 0:25 – 0:45  | Implement List & Search with pagination       | FR-2       |
| 0:45 – 1:05  | Implement Update + price history tracking     | FR-3       |
| 1:05 – 1:15  | Implement Soft Delete & Restore               | FR-4       |
| 1:15 – 1:30  | Implement Inventory Management                | FR-5       |
| 1:30 – 1:45  | Implement Analytics endpoints                 | FR-6       |
| 1:45 – 2:00  | Write tests, review, Q&A                      | All        |

---

*Document Version: 1.0 | Last Updated: 2025-01-15 | Faculty Development Program — AI-Native Software Development*
