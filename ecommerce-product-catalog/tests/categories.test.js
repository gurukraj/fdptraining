const request = require('supertest');
const app = require('../src/app');
const Category = require('../src/models/Category');
const Product = require('../src/models/Product');
const config = require('../src/config');
const Datastore = require('nedb-promises');

beforeAll(async () => {
  process.env.NODE_ENV = 'test';

  const productDb = Datastore.create();
  const categoryDb = Datastore.create();

  Product.setDb(productDb);
  Category.setDb(categoryDb);
});

beforeEach(async () => {
  await Category.removeAll();
});

afterAll(async () => {
  await Category.removeAll();
  await Product.removeAll();
});

describe('GET /api/categories', () => {
  test('should return all categories', async () => {
    // Seed categories first
    for (const name of config.validCategories) {
      await Category.create({ name, description: `${name} description` });
    }

    const res = await request(app)
      .get('/api/categories')
      .expect(200);

    expect(res.body.success).toBe(true);
    expect(res.body.data).toHaveLength(config.validCategories.length);

    const names = res.body.data.map((c) => c.name);
    for (const cat of config.validCategories) {
      expect(names).toContain(cat);
    }
  });

  test('should auto-seed categories if DB is empty', async () => {
    const res = await request(app)
      .get('/api/categories')
      .expect(200);

    expect(res.body.success).toBe(true);
    expect(res.body.data.length).toBeGreaterThan(0);
  });

  test('each category should have name and description', async () => {
    for (const name of config.validCategories) {
      await Category.create({ name, description: `${name} items` });
    }

    const res = await request(app)
      .get('/api/categories')
      .expect(200);

    res.body.data.forEach((cat) => {
      expect(cat).toHaveProperty('name');
      expect(cat).toHaveProperty('_id');
    });
  });
});
