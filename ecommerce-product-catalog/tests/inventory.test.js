const request = require('supertest');
const app = require('../src/app');
const Product = require('../src/models/Product');
const Category = require('../src/models/Category');
const config = require('../src/config');
const Datastore = require('nedb-promises');

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

describe('PATCH /api/products/:id/stock', () => {
  let productId;

  beforeEach(async () => {
    const res = await request(app)
      .post('/api/products')
      .send({ name: 'Stock Test Product', price: 20.00, category: 'Electronics', stock: 50 });
    productId = res.body.data._id;
  });

  test('should increase stock with positive adjustment', async () => {
    const res = await request(app)
      .patch(`/api/products/${productId}/stock`)
      .send({ adjustment: 10 })
      .expect(200);

    expect(res.body.success).toBe(true);
    expect(res.body.data.previousStock).toBe(50);
    expect(res.body.data.adjustment).toBe(10);
    expect(res.body.data.newStock).toBe(60);
  });

  test('should decrease stock with negative adjustment', async () => {
    const res = await request(app)
      .patch(`/api/products/${productId}/stock`)
      .send({ adjustment: -20 })
      .expect(200);

    expect(res.body.data.previousStock).toBe(50);
    expect(res.body.data.newStock).toBe(30);
  });

  test('should not allow stock to go below 0', async () => {
    const res = await request(app)
      .patch(`/api/products/${productId}/stock`)
      .send({ adjustment: -100 })
      .expect(400);

    expect(res.body.success).toBe(false);
    expect(res.body.error).toContain('Insufficient stock');
  });

  test('should return 422 for non-integer adjustment', async () => {
    const res = await request(app)
      .patch(`/api/products/${productId}/stock`)
      .send({ adjustment: 5.5 })
      .expect(422);

    expect(res.body.success).toBe(false);
  });

  test('should return 422 for missing adjustment', async () => {
    const res = await request(app)
      .patch(`/api/products/${productId}/stock`)
      .send({})
      .expect(422);

    expect(res.body.success).toBe(false);
  });

  test('should return 404 for non-existent product', async () => {
    const res = await request(app)
      .patch('/api/products/nonexistentid/stock')
      .send({ adjustment: 5 })
      .expect(404);

    expect(res.body.success).toBe(false);
  });
});

describe('GET /api/products/inventory/low-stock', () => {
  beforeEach(async () => {
    const products = [
      { name: 'Low Stock 1', price: 10.00, category: 'Electronics', stock: 2 },
      { name: 'Low Stock 2', price: 15.00, category: 'Clothing', stock: 5 },
      { name: 'Normal Stock', price: 20.00, category: 'Books', stock: 50 },
      { name: 'High Stock', price: 25.00, category: 'Toys', stock: 200 },
      { name: 'Zero Stock', price: 30.00, category: 'Sports', stock: 0 },
    ];
    for (const p of products) {
      await request(app).post('/api/products').send(p);
    }
  });

  test('should return products with stock at or below default threshold (10)', async () => {
    const res = await request(app)
      .get('/api/products/inventory/low-stock')
      .expect(200);

    expect(res.body.success).toBe(true);
    expect(res.body.data).toHaveLength(3); // stock 0, 2, 5
    res.body.data.forEach((p) => {
      expect(p.stock).toBeLessThanOrEqual(10);
    });
  });

  test('should use custom threshold', async () => {
    const res = await request(app)
      .get('/api/products/inventory/low-stock?threshold=3')
      .expect(200);

    expect(res.body.data).toHaveLength(2); // stock 0, 2
    res.body.data.forEach((p) => {
      expect(p.stock).toBeLessThanOrEqual(3);
    });
  });

  test('should sort by stock ascending', async () => {
    const res = await request(app)
      .get('/api/products/inventory/low-stock')
      .expect(200);

    for (let i = 1; i < res.body.data.length; i++) {
      expect(res.body.data[i].stock).toBeGreaterThanOrEqual(res.body.data[i - 1].stock);
    }
  });

  test('should include pagination info', async () => {
    const res = await request(app)
      .get('/api/products/inventory/low-stock')
      .expect(200);

    expect(res.body.pagination).toBeDefined();
    expect(res.body.pagination.totalCount).toBe(3);
  });
});
