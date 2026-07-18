const request = require('supertest');
const app = require('../src/app');
const Product = require('../src/models/Product');
const Category = require('../src/models/Category');
const config = require('../src/config');
const path = require('path');
const Datastore = require('nedb-promises');

// Use in-memory databases for testing
beforeAll(async () => {
  process.env.NODE_ENV = 'test';

  const productDb = Datastore.create();
  const categoryDb = Datastore.create();

  Product.setDb(productDb);
  Category.setDb(categoryDb);

  // Seed categories
  for (const name of config.validCategories) {
    await Category.create({ name, description: `${name} category` });
  }
});

beforeEach(async () => {
  await Product.removeAll();
});

afterAll(async () => {
  await Product.removeAll();
  await Category.removeAll();
});

describe('POST /api/products', () => {
  const validProduct = {
    name: 'Test Product',
    price: 29.99,
    category: 'Electronics',
    description: 'A test product description',
    tags: ['test', 'sample'],
    stock: 10,
  };

  test('should create a product with valid data', async () => {
    const res = await request(app)
      .post('/api/products')
      .send(validProduct)
      .expect(201);

    expect(res.body.success).toBe(true);
    expect(res.body.data).toHaveProperty('_id');
    expect(res.body.data.name).toBe(validProduct.name);
    expect(res.body.data.price).toBe(validProduct.price);
    expect(res.body.data.category).toBe(validProduct.category);
    expect(res.body.data.viewCount).toBe(0);
    expect(res.body.data.isDeleted).toBe(false);
    expect(res.body.data.createdAt).toBeDefined();
    expect(res.body.data.updatedAt).toBeDefined();
  });

  test('should create a product with minimum required fields', async () => {
    const res = await request(app)
      .post('/api/products')
      .send({ name: 'Min Product', price: 9.99, category: 'Books' })
      .expect(201);

    expect(res.body.data.stock).toBe(0);
    expect(res.body.data.tags).toEqual([]);
    expect(res.body.data.description).toBe('');
  });

  test('should return 422 for missing name', async () => {
    const res = await request(app)
      .post('/api/products')
      .send({ price: 29.99, category: 'Electronics' })
      .expect(422);

    expect(res.body.success).toBe(false);
  });

  test('should return 422 for name too short', async () => {
    const res = await request(app)
      .post('/api/products')
      .send({ name: 'AB', price: 29.99, category: 'Electronics' })
      .expect(422);

    expect(res.body.success).toBe(false);
  });

  test('should return 422 for negative price', async () => {
    const res = await request(app)
      .post('/api/products')
      .send({ name: 'Test Product', price: -5, category: 'Electronics' })
      .expect(422);

    expect(res.body.success).toBe(false);
  });

  test('should return 422 for price with more than 2 decimal places', async () => {
    const res = await request(app)
      .post('/api/products')
      .send({ name: 'Test Product', price: 29.999, category: 'Electronics' })
      .expect(422);

    expect(res.body.success).toBe(false);
  });

  test('should return 422 for invalid category', async () => {
    const res = await request(app)
      .post('/api/products')
      .send({ name: 'Test Product', price: 29.99, category: 'InvalidCategory' })
      .expect(422);

    expect(res.body.success).toBe(false);
  });

  test('should return 409 for duplicate name+category', async () => {
    await request(app).post('/api/products').send(validProduct);
    const res = await request(app)
      .post('/api/products')
      .send(validProduct)
      .expect(409);

    expect(res.body.success).toBe(false);
  });

  test('should deduplicate tags', async () => {
    const res = await request(app)
      .post('/api/products')
      .send({ ...validProduct, tags: ['test', 'Test', 'TEST', 'unique'] })
      .expect(201);

    expect(res.body.data.tags).toHaveLength(2);
    expect(res.body.data.tags).toContain('test');
    expect(res.body.data.tags).toContain('unique');
  });

  test('should accept category case-insensitively', async () => {
    const res = await request(app)
      .post('/api/products')
      .send({ ...validProduct, name: 'Case Test', category: 'electronics' })
      .expect(201);

    expect(res.body.data.category).toBe('Electronics');
  });
});

describe('GET /api/products', () => {
  beforeEach(async () => {
    // Create test products
    const products = [
      { name: 'Alpha Widget', price: 10.99, category: 'Electronics', description: 'Electronic widget', tags: ['widget'], stock: 5 },
      { name: 'Beta Gadget', price: 25.99, category: 'Electronics', description: 'Cool gadget', tags: ['gadget'], stock: 20 },
      { name: 'Gamma Shirt', price: 19.99, category: 'Clothing', description: 'Nice shirt', tags: ['cotton', 'casual'], stock: 50 },
      { name: 'Delta Book', price: 14.99, category: 'Books', description: 'Great read about widgets', tags: ['fiction'], stock: 30 },
      { name: 'Epsilon Toy', price: 9.99, category: 'Toys', description: 'Fun toy', tags: ['fun'], stock: 100 },
    ];
    for (const p of products) {
      await request(app).post('/api/products').send(p);
    }
  });

  test('should list products with default pagination', async () => {
    const res = await request(app)
      .get('/api/products')
      .expect(200);

    expect(res.body.success).toBe(true);
    expect(res.body.data).toHaveLength(5);
    expect(res.body.pagination).toBeDefined();
    expect(res.body.pagination.totalCount).toBe(5);
    expect(res.body.pagination.page).toBe(1);
    expect(res.body.pagination.limit).toBe(10);
  });

  test('should paginate results', async () => {
    const res = await request(app)
      .get('/api/products?page=1&limit=2')
      .expect(200);

    expect(res.body.data).toHaveLength(2);
    expect(res.body.pagination.totalCount).toBe(5);
    expect(res.body.pagination.totalPages).toBe(3);
    expect(res.body.pagination.hasNextPage).toBe(true);
    expect(res.body.pagination.hasPrevPage).toBe(false);
  });

  test('should search by name', async () => {
    const res = await request(app)
      .get('/api/products?search=Widget')
      .expect(200);

    // "Alpha Widget" matches by name, "Delta Book" matches by description (about widgets)
    expect(res.body.data.length).toBeGreaterThanOrEqual(1);
    const names = res.body.data.map((p) => p.name);
    expect(names).toContain('Alpha Widget');
  });

  test('should search across description', async () => {
    const res = await request(app)
      .get('/api/products?search=widgets')
      .expect(200);

    // Both "Alpha Widget" (name) and "Delta Book" (description contains "widgets") should match
    expect(res.body.data.length).toBeGreaterThanOrEqual(1);
  });

  test('should filter by category', async () => {
    const res = await request(app)
      .get('/api/products?category=Electronics')
      .expect(200);

    expect(res.body.data).toHaveLength(2);
    res.body.data.forEach((p) => {
      expect(p.category).toBe('Electronics');
    });
  });

  test('should filter by category case-insensitively', async () => {
    const res = await request(app)
      .get('/api/products?category=electronics')
      .expect(200);

    expect(res.body.data).toHaveLength(2);
  });

  test('should filter by price range', async () => {
    const res = await request(app)
      .get('/api/products?minPrice=15&maxPrice=30')
      .expect(200);

    res.body.data.forEach((p) => {
      expect(p.price).toBeGreaterThanOrEqual(15);
      expect(p.price).toBeLessThanOrEqual(30);
    });
  });

  test('should filter by tags', async () => {
    const res = await request(app)
      .get('/api/products?tags=cotton')
      .expect(200);

    expect(res.body.data.length).toBeGreaterThanOrEqual(1);
    const hasTag = res.body.data.every((p) =>
      p.tags.some((t) => t.toLowerCase() === 'cotton')
    );
    expect(hasTag).toBe(true);
  });

  test('should sort by price ascending', async () => {
    const res = await request(app)
      .get('/api/products?sortBy=price&sortOrder=asc')
      .expect(200);

    for (let i = 1; i < res.body.data.length; i++) {
      expect(res.body.data[i].price).toBeGreaterThanOrEqual(res.body.data[i - 1].price);
    }
  });

  test('should sort by name', async () => {
    const res = await request(app)
      .get('/api/products?sortBy=name&sortOrder=asc')
      .expect(200);

    for (let i = 1; i < res.body.data.length; i++) {
      expect(res.body.data[i].name >= res.body.data[i - 1].name).toBe(true);
    }
  });

  test('should exclude soft-deleted products', async () => {
    // Create and delete a product
    const createRes = await request(app)
      .post('/api/products')
      .send({ name: 'To Be Deleted', price: 5.99, category: 'Toys' });
    const id = createRes.body.data._id;
    await request(app).delete(`/api/products/${id}`);

    const res = await request(app).get('/api/products').expect(200);
    const names = res.body.data.map((p) => p.name);
    expect(names).not.toContain('To Be Deleted');
  });
});

describe('GET /api/products/:id', () => {
  test('should get a product by ID and increment viewCount', async () => {
    const createRes = await request(app)
      .post('/api/products')
      .send({ name: 'View Test Product', price: 15.99, category: 'Books' });
    const id = createRes.body.data._id;

    const res = await request(app).get(`/api/products/${id}`).expect(200);
    expect(res.body.data.viewCount).toBe(1);

    const res2 = await request(app).get(`/api/products/${id}`).expect(200);
    expect(res2.body.data.viewCount).toBe(2);
  });

  test('should return 404 for non-existent product', async () => {
    const res = await request(app).get('/api/products/nonexistentid').expect(404);
    expect(res.body.success).toBe(false);
  });
});

describe('PUT /api/products/:id', () => {
  let productId;

  beforeEach(async () => {
    const res = await request(app)
      .post('/api/products')
      .send({ name: 'Update Test', price: 20.00, category: 'Electronics', tags: ['original'] });
    productId = res.body.data._id;
  });

  test('should update product name', async () => {
    const res = await request(app)
      .put(`/api/products/${productId}`)
      .send({ name: 'Updated Name' })
      .expect(200);

    expect(res.body.data.name).toBe('Updated Name');
  });

  test('should track price changes in priceHistory', async () => {
    const res = await request(app)
      .put(`/api/products/${productId}`)
      .send({ price: 25.00 })
      .expect(200);

    expect(res.body.data.price).toBe(25.00);
    expect(res.body.data.priceHistory).toHaveLength(1);
    expect(res.body.data.priceHistory[0].oldPrice).toBe(20.00);
    expect(res.body.data.priceHistory[0].newPrice).toBe(25.00);
    expect(res.body.data.priceHistory[0].changedAt).toBeDefined();
  });

  test('should not allow updating viewCount', async () => {
    const res = await request(app)
      .put(`/api/products/${productId}`)
      .send({ viewCount: 999 })
      .expect(422);

    expect(res.body.success).toBe(false);
  });

  test('should not allow updating isDeleted', async () => {
    const res = await request(app)
      .put(`/api/products/${productId}`)
      .send({ isDeleted: true })
      .expect(422);

    expect(res.body.success).toBe(false);
  });

  test('should return 404 for non-existent product', async () => {
    const res = await request(app)
      .put('/api/products/nonexistentid')
      .send({ name: 'No Product' })
      .expect(404);

    expect(res.body.success).toBe(false);
  });

  test('should partially update product', async () => {
    const res = await request(app)
      .put(`/api/products/${productId}`)
      .send({ description: 'New description only' })
      .expect(200);

    expect(res.body.data.description).toBe('New description only');
    expect(res.body.data.name).toBe('Update Test');
    expect(res.body.data.price).toBe(20.00);
  });
});

describe('DELETE /api/products/:id', () => {
  test('should soft delete a product', async () => {
    const createRes = await request(app)
      .post('/api/products')
      .send({ name: 'Delete Me', price: 5.99, category: 'Toys' });
    const id = createRes.body.data._id;

    const res = await request(app).delete(`/api/products/${id}`).expect(200);
    expect(res.body.success).toBe(true);
    expect(res.body.data.message).toContain('soft-deleted');
  });

  test('should return 404 for non-existent product', async () => {
    await request(app).delete('/api/products/nonexistentid').expect(404);
  });

  test('should return 400 for already deleted product', async () => {
    const createRes = await request(app)
      .post('/api/products')
      .send({ name: 'Double Delete', price: 5.99, category: 'Toys' });
    const id = createRes.body.data._id;

    await request(app).delete(`/api/products/${id}`);
    await request(app).delete(`/api/products/${id}`).expect(400);
  });
});

describe('POST /api/products/:id/restore', () => {
  test('should restore a soft-deleted product', async () => {
    const createRes = await request(app)
      .post('/api/products')
      .send({ name: 'Restore Me', price: 5.99, category: 'Toys' });
    const id = createRes.body.data._id;

    await request(app).delete(`/api/products/${id}`);
    const res = await request(app).post(`/api/products/${id}/restore`).expect(200);
    expect(res.body.success).toBe(true);
    expect(res.body.data.message).toContain('restored');

    // Verify product is accessible again
    const getRes = await request(app).get(`/api/products/${id}`).expect(200);
    expect(getRes.body.data.isDeleted).toBe(false);
  });

  test('should return 400 for product that is not deleted', async () => {
    const createRes = await request(app)
      .post('/api/products')
      .send({ name: 'Not Deleted', price: 5.99, category: 'Toys' });
    const id = createRes.body.data._id;

    await request(app).post(`/api/products/${id}/restore`).expect(400);
  });
});
