# E-Commerce Product Catalog API

## What You'll Build

A RESTful product catalog API for an e-commerce platform, supporting full CRUD operations, inventory management with low-stock alerts, flexible search and filtering, soft-delete with restore, and product analytics.

**Scenario:** An e-commerce startup is building its backend from scratch. The product team needs a catalog service that handles product listings, tracks inventory levels, and provides analytics dashboards showing category breakdowns, price distributions, and most-viewed items. Products must never be hard-deleted — only soft-deleted with the ability to restore.

## Technology Stack

| Component     | Technology                        |
|---------------|-----------------------------------|
| Runtime       | Node.js 20                        |
| Framework     | Express                           |
| Database      | NeDB (embedded document database) |
| Validation    | express-validator                  |
| Testing       | Jest or Mocha                      |

## Functional Requirements

| FR-ID | Title                 | Description                                                                                          | Key Acceptance Criteria                                                                                     |
|-------|-----------------------|------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| FR-1  | Create Product        | Add a new product to the catalog with full validation.                                               | `name` 3-200 chars; `price` > 0 with max 2 decimals; `sku` unique (409 on duplicate); `category` must be a valid predefined category; `tags` is an array; `imageUrl` is optional. |
| FR-2  | List & Search         | Retrieve products with pagination, filtering, keyword search, and sorting.                           | Supports `page`/`limit` pagination; filter by `category`, `priceMin`, `priceMax`, `inStock`; search across `name`/`description`; sort by `price`, `name`, or `createdAt`. |
| FR-3  | Update Product        | Apply partial updates to an existing product, re-validating all changed fields.                      | Only provided fields are updated; same validation rules as creation apply; returns **404** if product does not exist. |
| FR-4  | Soft Delete & Restore | Mark a product as deleted without removing it; exclude soft-deleted products from standard listings.  | DELETE sets `isDeleted: true`; soft-deleted products are hidden from GET listings; a restore endpoint reverses the deletion. |
| FR-5  | Manage Inventory      | Adjust stock quantities up or down; prevent negative stock; flag low-stock products.                 | Stock adjustment via signed integer (+/-); stock cannot go below 0 (return **400**); low-stock threshold defaults to 10, configurable via query param. |
| FR-6  | Product Analytics     | Provide analytics: most-viewed products, category breakdown, and price distribution.                 | Most-viewed returns top N products by `viewCount`; category breakdown shows count and average price per category; price distribution groups products into defined ranges. |

## Predefined Categories

Electronics, Clothing, Books, Home & Kitchen, Sports, Toys, Beauty, Food & Beverages

## API Endpoints Summary

| Method | Path                                   | Description                                      | Success | Error Codes     |
|--------|----------------------------------------|--------------------------------------------------|---------|-----------------|
| POST   | `/api/products`                        | Create a new product                             | 201     | 400, 409, 422   |
| GET    | `/api/products`                        | List products with search, filter, sort, paginate| 200     | 400             |
| GET    | `/api/products/:id`                    | Get a single product by ID (increments viewCount)| 200     | 404             |
| PUT    | `/api/products/:id`                    | Update a product                                 | 200     | 400, 404, 422   |
| DELETE | `/api/products/:id`                    | Soft-delete a product                            | 200     | 404             |
| POST   | `/api/products/:id/restore`            | Restore a soft-deleted product                   | 200     | 404             |
| PATCH  | `/api/products/:id/stock`              | Adjust stock quantity (+/-)                      | 200     | 400, 404        |
| GET    | `/api/products/inventory/low-stock`    | List products below stock threshold              | 200     | -               |
| GET    | `/api/analytics/most-viewed`           | Top products by view count                       | 200     | -               |
| GET    | `/api/analytics/category-breakdown`    | Product count and average price per category     | 200     | -               |
| GET    | `/api/analytics/price-distribution`    | Product counts grouped by price range            | 200     | -               |

## Data Model

### Product

| Field         | Type      | Constraints                                    |
|---------------|-----------|------------------------------------------------|
| _id           | String    | Auto-generated by NeDB                         |
| name          | String    | Required, 3-200 characters                     |
| description   | String    | Optional                                       |
| price         | Number    | Required, > 0, max 2 decimal places            |
| sku           | String    | Required, unique                               |
| category      | String    | Required, must be a predefined category         |
| tags          | Array     | Array of strings, default empty                |
| stockQuantity | Integer   | Default 0, cannot be negative                  |
| imageUrl      | String    | Optional, valid URL format                     |
| viewCount     | Integer   | Default 0, incremented on product detail view  |
| isDeleted     | Boolean   | Default false                                  |
| createdAt     | DateTime  | Auto-set on creation                           |
| updatedAt     | DateTime  | Auto-set on creation and update                |

### Category

Categories are predefined (see list above). Validation should reject any product whose `category` field does not match one of the predefined values.

## Price Distribution Ranges

Analytics should group products into these price ranges: $0-25, $25-50, $50-100, $100-250, $250-500, $500+.

## Success Criteria

- All 11 endpoints return correct status codes and response structures.
- Product creation validates all field constraints; duplicate SKU returns 409.
- Listing endpoint supports pagination, all filters, keyword search, and multi-field sorting.
- Soft-deleted products are excluded from listings and search results but can be restored.
- Stock adjustments correctly increment/decrement and reject operations that would result in negative stock.
- Viewing a product detail increments its `viewCount`.
- Analytics endpoints return accurate aggregations over the current (non-deleted) product set.
- Application starts cleanly and NeDB datastores initialize without manual setup.
- Seed data with at least 10 products across multiple categories can be loaded and queried.
