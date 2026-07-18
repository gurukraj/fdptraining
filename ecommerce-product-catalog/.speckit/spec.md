# E-Commerce Product Catalog API - SDD Specification

## Overview
REST API for managing an e-commerce product catalog supporting CRUD operations, inventory management, full-text search, filtering, and product analytics.

## Functional Requirements

### FR-1: Product CRUD
- **Create** (POST /api/products): Validate name (3-200 chars), price (positive, 2 decimal max), category (must exist), optional description/tags/imageUrl/stock. Duplicate name+category returns 409.
- **Read** (GET /api/products/:id): Returns product, increments viewCount.
- **Update** (PUT /api/products/:id): Partial update, price changes tracked in priceHistory. Cannot modify viewCount or isDeleted.
- **Delete** (DELETE /api/products/:id): Soft delete (isDeleted=true, deletedAt set).
- **Restore** (POST /api/products/:id/restore): Restores soft-deleted product.

### FR-2: Search & Filter
- Full-text search across name and description via `?search=`
- Filters: category, minPrice, maxPrice, tags (comma-separated, ANY match)
- Pagination: page (default 1), limit (default 10, max 100)
- Sort: sortBy (price|name|createdAt|viewCount), sortOrder (asc|desc)
- Excludes soft-deleted products

### FR-3: Inventory Management
- PATCH /api/products/:id/stock: Adjust stock with `{ adjustment: N }` (positive or negative)
- Stock cannot go below 0
- GET /api/products/inventory/low-stock?threshold=10: Low stock alerts

### FR-4: Product Analytics
- GET /api/analytics/most-viewed?limit=10: Top viewed products
- GET /api/analytics/category-breakdown: Count and avg price per category
- GET /api/analytics/price-distribution: Min, max, avg, median price stats

## Data Models

### Product
| Field | Type | Constraints |
|-------|------|-------------|
| _id | string | Auto-generated |
| name | string | 3-200 chars, required |
| description | string | Max 5000 chars |
| price | number | Positive, max 2 decimals |
| category | string | Must exist in categories |
| tags | array[string] | Max 10, each 1-50 chars, deduplicated |
| imageUrl | string | Valid URL |
| stock | integer | Non-negative, default 0 |
| viewCount | integer | Default 0 |
| priceHistory | array[object] | {oldPrice, newPrice, changedAt} |
| isDeleted | boolean | Default false |
| deletedAt | date | Set on soft delete |
| createdAt | date | Auto-set |
| updatedAt | date | Auto-updated |

### Category
| Field | Type | Constraints |
|-------|------|-------------|
| _id | string | Auto-generated |
| name | string | Unique, required |
| description | string | Optional |

## Response Format
```json
{
  "success": true,
  "data": {},
  "pagination": {
    "totalCount": 50,
    "page": 1,
    "limit": 10,
    "totalPages": 5,
    "hasNextPage": true,
    "hasPrevPage": false
  }
}
```
