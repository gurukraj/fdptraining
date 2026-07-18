# E-Commerce Product Catalog API

A comprehensive RESTful API for managing an e-commerce product catalog with full CRUD operations, inventory management, search/filtering, and analytics.

## Quick Start

### Prerequisites
- Node.js 20+
- npm

### Setup

```bash
# Install dependencies
npm install

# Seed the database with sample data (55 products, 8 categories)
npm run seed

# Start the server
npm start

# Or start in development mode (auto-restart on changes)
npm run dev

# Run tests
npm test
```

The API will be running at `http://localhost:3000`.

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| PORT | 3000 | Server port |
| NODE_ENV | development | Environment (development/test/production) |

## API Endpoints

### Health Check
```
GET /api/health
```

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/products | Create a new product |
| GET | /api/products | List & search products |
| GET | /api/products/:id | Get product (increments view count) |
| PUT | /api/products/:id | Update product |
| DELETE | /api/products/:id | Soft delete product |
| POST | /api/products/:id/restore | Restore soft-deleted product |

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/categories | List all categories |

### Inventory

| Method | Endpoint | Description |
|--------|----------|-------------|
| PATCH | /api/products/:id/stock | Adjust product stock |
| GET | /api/products/inventory/low-stock | Get low-stock products |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/analytics/most-viewed | Most viewed products |
| GET | /api/analytics/category-breakdown | Category stats |
| GET | /api/analytics/price-distribution | Price distribution |

## API Examples

### Create a Product
```bash
curl -X POST http://localhost:3000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Headphones",
    "price": 79.99,
    "category": "Electronics",
    "description": "Premium noise-cancelling headphones",
    "tags": ["wireless", "bluetooth"],
    "stock": 100
  }'
```

### Search Products
```bash
# Full-text search
curl "http://localhost:3000/api/products?search=wireless"

# Filter by category and price range
curl "http://localhost:3000/api/products?category=Electronics&minPrice=20&maxPrice=100"

# Sort by price ascending, page 2
curl "http://localhost:3000/api/products?sortBy=price&sortOrder=asc&page=2&limit=5"

# Filter by tags
curl "http://localhost:3000/api/products?tags=bluetooth,wireless"
```

### Update a Product
```bash
curl -X PUT http://localhost:3000/api/products/<id> \
  -H "Content-Type: application/json" \
  -d '{"price": 69.99}'
```

### Adjust Stock
```bash
curl -X PATCH http://localhost:3000/api/products/<id>/stock \
  -H "Content-Type: application/json" \
  -d '{"adjustment": -5}'
```

### Get Low Stock Products
```bash
curl "http://localhost:3000/api/products/inventory/low-stock?threshold=10"
```

### Analytics
```bash
# Most viewed products
curl "http://localhost:3000/api/analytics/most-viewed?limit=5"

# Category breakdown
curl "http://localhost:3000/api/analytics/category-breakdown"

# Price distribution
curl "http://localhost:3000/api/analytics/price-distribution"
```

## Response Format

All responses follow a consistent format:

```json
{
  "success": true,
  "data": { ... },
  "pagination": {
    "totalCount": 55,
    "page": 1,
    "limit": 10,
    "totalPages": 6,
    "hasNextPage": true,
    "hasPrevPage": false
  }
}
```

Error responses:
```json
{
  "success": false,
  "error": "Error message",
  "errors": [...]
}
```

## Running Tests

```bash
# Run all tests with coverage
npm test

# Tests include:
# - Product CRUD operations
# - Search and filtering
# - Pagination and sorting
# - Input validation
# - Inventory management
# - Analytics endpoints
```

## Project Structure

```
ecommerce-product-catalog/
├── .speckit/           # SDD specification files
├── src/
│   ├── app.js          # Express app setup
│   ├── server.js       # Server entry point
│   ├── config/         # Configuration
│   ├── models/         # Data models (nedb-promises)
│   ├── routes/         # API route handlers
│   ├── middleware/      # Error handling & validation
│   ├── services/       # Business logic
│   └── utils/          # Helper functions
├── tests/              # Jest integration tests
├── data/               # Sample data & seed script
└── docs
```

## Categories

The API supports these product categories:
- Electronics
- Clothing
- Books
- Home & Kitchen
- Sports
- Toys
- Beauty
- Food & Beverages
