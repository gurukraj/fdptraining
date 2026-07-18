const path = require('path');

const config = {
  port: process.env.PORT || 3000,
  env: process.env.NODE_ENV || 'development',
  db: {
    productsPath: process.env.DB_PRODUCTS_PATH || path.join(__dirname, '../../data/products.db'),
    categoriesPath: process.env.DB_CATEGORIES_PATH || path.join(__dirname, '../../data/categories.db'),
  },
  pagination: {
    defaultPage: 1,
    defaultLimit: 10,
    maxLimit: 100,
  },
  validation: {
    nameMinLength: 3,
    nameMaxLength: 200,
    descriptionMaxLength: 5000,
    maxTags: 10,
    tagMinLength: 1,
    tagMaxLength: 50,
    maxPriceDecimals: 2,
  },
  validCategories: [
    'Electronics',
    'Clothing',
    'Books',
    'Home & Kitchen',
    'Sports',
    'Toys',
    'Beauty',
    'Food & Beverages',
  ],
};

module.exports = config;
