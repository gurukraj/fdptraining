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

describe('View Count (GET /api/products/:id)', () => {
  test('should increment viewCount on each GET', async () => {
    const createRes = await request(app)
      .post('/api/products')
      .send({ name: 'View Counter Test', price: 10.00, category: 'Electronics' });
    const id = createRes.body.data._id;

    // View 3 times
    await request(app).get(`/api/products/${id}`);
    await request(app).get(`/api/products/${id}`);
    const res = await request(app).get(`/api/products/${id}`).expect(200);

    expect(res.body.data.viewCount).toBe(3);
  });
});

describe('GET /api/analytics/most-viewed', () => {
  beforeEach(async () => {
    // Create products and simulate views
    const products = [
      { name: 'Popular Item', price: 10.00, category: 'Electronics' },
      { name: 'Medium Item', price: 20.00, category: 'Clothing' },
      { name: 'Unpopular Item', price: 30.00, category: 'Books' },
    ];

    const ids = [];
    for (const p of products) {
      const res = await request(app).post('/api/products').send(p);
      ids.push(res.body.data._id);
    }

    // Simulate views: Popular=5, Medium=2, Unpopular=0
    for (let i = 0; i < 5; i++) await request(app).get(`/api/products/${ids[0]}`);
    for (let i = 0; i < 2; i++) await request(app).get(`/api/products/${ids[1]}`);
  });

  test('should return most viewed products sorted by viewCount desc', async () => {
    const res = await request(app)
      .get('/api/analytics/most-viewed')
      .expect(200);

    expect(res.body.success).toBe(true);
    expect(res.body.data.length).toBeGreaterThanOrEqual(2);
    expect(res.body.data[0].viewCount).toBeGreaterThanOrEqual(res.body.data[1].viewCount);
  });

  test('should respect limit parameter', async () => {
    const res = await request(app)
      .get('/api/analytics/most-viewed?limit=2')
      .expect(200);

    expect(res.body.data).toHaveLength(2);
  });

  test('should return the most popular item first', async () => {
    const res = await request(app)
      .get('/api/analytics/most-viewed')
      .expect(200);

    expect(res.body.data[0].name).toBe('Popular Item');
    expect(res.body.data[0].viewCount).toBe(5);
  });
});

describe('GET /api/analytics/category-breakdown', () => {
  beforeEach(async () => {
    const products = [
      { name: 'Elec 1', price: 100.00, category: 'Electronics' },
      { name: 'Elec 2', price: 200.00, category: 'Electronics' },
      { name: 'Cloth 1', price: 50.00, category: 'Clothing' },
      { name: 'Book 1', price: 20.00, category: 'Books' },
      { name: 'Book 2', price: 30.00, category: 'Books' },
      { name: 'Book 3', price: 40.00, category: 'Books' },
    ];
    for (const p of products) {
      await request(app).post('/api/products').send(p);
    }
  });

  test('should return category breakdown with count and average price', async () => {
    const res = await request(app)
      .get('/api/analytics/category-breakdown')
      .expect(200);

    expect(res.body.success).toBe(true);
    expect(res.body.data.length).toBeGreaterThanOrEqual(3);

    const electronics = res.body.data.find((c) => c.category === 'Electronics');
    expect(electronics).toBeDefined();
    expect(electronics.count).toBe(2);
    expect(electronics.averagePrice).toBe(150.00);

    const books = res.body.data.find((c) => c.category === 'Books');
    expect(books).toBeDefined();
    expect(books.count).toBe(3);
    expect(books.averagePrice).toBe(30.00);
  });

  test('should sort by count descending', async () => {
    const res = await request(app)
      .get('/api/analytics/category-breakdown')
      .expect(200);

    for (let i = 1; i < res.body.data.length; i++) {
      expect(res.body.data[i].count).toBeLessThanOrEqual(res.body.data[i - 1].count);
    }
  });
});

describe('GET /api/analytics/price-distribution', () => {
  beforeEach(async () => {
    const products = [
      { name: 'Cheap', price: 10.00, category: 'Electronics' },
      { name: 'Mid Low', price: 20.00, category: 'Clothing' },
      { name: 'Mid', price: 30.00, category: 'Books' },
      { name: 'Mid High', price: 40.00, category: 'Toys' },
      { name: 'Expensive', price: 50.00, category: 'Sports' },
    ];
    for (const p of products) {
      await request(app).post('/api/products').send(p);
    }
  });

  test('should return price distribution stats', async () => {
    const res = await request(app)
      .get('/api/analytics/price-distribution')
      .expect(200);

    expect(res.body.success).toBe(true);
    expect(res.body.data.totalProducts).toBe(5);
    expect(res.body.data.min).toBe(10.00);
    expect(res.body.data.max).toBe(50.00);
    expect(res.body.data.average).toBe(30.00);
    expect(res.body.data.median).toBe(30.00);
  });

  test('should handle empty product list', async () => {
    await Product.removeAll();

    const res = await request(app)
      .get('/api/analytics/price-distribution')
      .expect(200);

    expect(res.body.data.totalProducts).toBe(0);
    expect(res.body.data.min).toBe(0);
    expect(res.body.data.max).toBe(0);
    expect(res.body.data.average).toBe(0);
    expect(res.body.data.median).toBe(0);
  });
});
