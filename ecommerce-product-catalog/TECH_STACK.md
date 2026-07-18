# Technology Stack - E-Commerce Product Catalog API

## Runtime: Node.js 20+

**Why Node.js 20+?**
- Modern JavaScript features (ES modules, top-level await, structuredClone)
- Native watch mode (`node --watch`) for development without extra tooling
- Excellent async I/O performance, ideal for API servers
- Massive npm ecosystem for rapid development
- Single language (JavaScript) across the entire stack
- LTS support with long-term stability guarantees

## Framework: Express.js 4.x

**Why Express?**
- **Minimal & Unopinionated**: Doesn't impose architecture decisions, allowing clean separation of concerns
- **Middleware-Based**: Composable middleware pipeline for request processing (parsing, validation, auth, error handling)
- **Fast**: Thin abstraction over Node.js HTTP, minimal overhead
- **Massive Ecosystem**: Thousands of middleware packages (cors, helmet, morgan, express-validator)
- **Battle-Tested**: Most widely used Node.js framework, mature and stable
- **Easy to Learn**: Simple API that maps directly to HTTP concepts

### Key Middleware Used
- **helmet**: Sets security-related HTTP headers (X-Content-Type-Options, X-Frame-Options, CSP, etc.)
- **cors**: Configures Cross-Origin Resource Sharing for browser clients
- **morgan**: HTTP request logging for debugging and monitoring
- **express-validator**: Declarative input validation with chainable API

## Database: nedb-promises (Embedded Document DB)

**Why nedb-promises?**
- **MongoDB-Compatible API**: Uses the same query syntax (find, insert, update, remove, $operators)
- **Zero Configuration**: No database server required - runs embedded in the Node.js process
- **Portable**: Database stored as flat files, easy to share, backup, and version control
- **Perfect for Workshops**: No installation steps, works on any machine with Node.js
- **Easy Migration Path**: Architecture uses the same patterns as Mongoose/MongoDB, making migration trivial

**Why a Document Database for Product Catalogs?**
- **Flexible Schemas**: Products have varying attributes (electronics have specs, clothing has sizes)
- **Nested Objects**: Natural storage for arrays (tags, priceHistory) without join tables
- **JSON-Native**: Products are inherently JSON documents - no impedance mismatch
- **Denormalized Reads**: Product listing pages get all data in a single read
- **Schema Evolution**: Easy to add new fields without migrations

### nedb Query Examples (MongoDB-compatible)
```javascript
// Find products in a category
db.find({ category: 'Electronics', isDeleted: false })

// Price range query
db.find({ price: { $gte: 10, $lte: 100 } })

// Regex search
db.find({ name: /wireless/i })

// Update with operators
db.update({ _id: id }, { $set: { price: 99.99 }, $push: { priceHistory: entry } })
```

## Testing: Jest + Supertest

**Why Jest?**
- **All-in-One**: Test runner, assertion library, mocking, and coverage in a single package
- **Fast**: Parallel test execution with worker processes
- **Rich Assertions**: `expect().toBe()`, `toHaveProperty()`, `toContain()`, etc.
- **Mocking**: Built-in module mocking and spy functions
- **Coverage**: Built-in Istanbul coverage reporting (`--coverage` flag)
- **Watch Mode**: Re-runs tests on file changes during development

**Why Supertest?**
- **HTTP Integration Testing**: Tests the full request/response cycle
- **Express Integration**: Direct integration with Express apps (no server needed)
- **Chainable API**: Fluent interface for building requests and asserting responses
- **Real HTTP Semantics**: Tests headers, status codes, body parsing - the same things clients experience

## Validation: express-validator

**Why express-validator?**
- **Declarative**: Validation rules read like documentation
- **Chainable**: `body('price').isFloat({ gt: 0 }).withMessage('Must be positive')`
- **Middleware-Native**: Integrates naturally into Express route middleware chains
- **Comprehensive**: Built on validator.js with 70+ validators (isEmail, isURL, isISO8601, etc.)
- **Custom Validators**: Easy to add domain-specific rules
- **Sanitization**: Built-in sanitizers (trim, escape, toInt) to clean input data

## Architecture Pattern: Service Layer

```
Request → Route → Validator Middleware → Service → Model → Database
                                              ↓
Response ← Route ← Error Handler Middleware ←─┘
```

**Why Service Layer?**
- **Separation of Concerns**: Routes handle HTTP, services handle business logic, models handle data
- **Testability**: Services can be tested independently of HTTP
- **Reusability**: Same service methods can be used by different routes or future GraphQL/gRPC APIs
- **Maintainability**: Changes to business rules are isolated to service layer

## Security

- **Helmet**: Automatic security headers
- **Input Validation**: All inputs validated before processing
- **Soft Delete**: Data preservation for audit trails
- **Error Handling**: Centralized error handler prevents information leakage
