# E-Commerce Product Catalog API - Project Constitution

## Project Identity
- **Name**: E-Commerce Product Catalog API
- **Type**: RESTful API Service
- **Version**: 1.0.0

## Mission Statement
Provide a robust, well-structured REST API for managing an e-commerce product catalog with full CRUD operations, inventory management, search/filtering, and analytics capabilities.

## Core Principles
1. **Clean Architecture**: Separation of concerns with distinct layers (routes, services, models)
2. **Data Integrity**: Comprehensive input validation and error handling
3. **Soft Delete Pattern**: Products are never permanently deleted; soft-delete preserves data integrity
4. **Auditability**: Price history tracking, timestamps on all mutations
5. **Portability**: Uses embedded document DB (nedb-promises) for zero-config setup

## Technology Decisions
- **Runtime**: Node.js 20+
- **Framework**: Express.js 4.x
- **Database**: nedb-promises (MongoDB-compatible embedded document DB)
- **Validation**: express-validator
- **Testing**: Jest + supertest
- **Security**: helmet for HTTP headers, cors for cross-origin

## Architecture Pattern
- **Pattern**: Service Layer Architecture
- **Flow**: Route → Validator → Service → Model → Database
- **Error Handling**: Centralized middleware-based error handling

## API Design Principles
- RESTful resource naming
- Consistent JSON response format: `{ success, data, pagination?, error? }`
- HTTP status codes used correctly (201 Created, 409 Conflict, 422 Validation, etc.)
- Pagination on all list endpoints
