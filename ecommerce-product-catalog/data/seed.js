const path = require('path');
const Datastore = require('nedb-promises');

const productsData = require('./products.json');
const categoriesData = require('./categories.json');

async function seed() {
  console.log('Seeding database...\n');

  // Initialize datastores
  const productsDb = Datastore.create({
    filename: path.join(__dirname, 'products.db'),
    autoload: true,
  });

  const categoriesDb = Datastore.create({
    filename: path.join(__dirname, 'categories.db'),
    autoload: true,
  });

  // Clear existing data
  await productsDb.remove({}, { multi: true });
  await categoriesDb.remove({}, { multi: true });
  console.log('Cleared existing data.');

  // Seed categories
  const now = new Date().toISOString();
  for (const category of categoriesData) {
    await categoriesDb.insert({
      ...category,
      createdAt: now,
      updatedAt: now,
    });
  }
  console.log(`Seeded ${categoriesData.length} categories.`);

  // Seed products
  for (const product of productsData) {
    await productsDb.insert({
      ...product,
      stock: product.stock || 0,
      viewCount: 0,
      priceHistory: [],
      isDeleted: false,
      deletedAt: null,
      createdAt: now,
      updatedAt: now,
    });
  }
  console.log(`Seeded ${productsData.length} products.`);

  console.log('\nDatabase seeding completed successfully!');
}

seed().catch((err) => {
  console.error('Seeding failed:', err);
  process.exit(1);
});
