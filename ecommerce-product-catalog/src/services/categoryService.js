const Category = require('../models/Category');
const config = require('../config');

/**
 * Get all categories.
 * If DB is empty, seed with default categories from config.
 */
async function getAllCategories() {
  let categories = await Category.findAll();

  if (categories.length === 0) {
    // Seed default categories
    for (const name of config.validCategories) {
      try {
        await Category.create({ name, description: '' });
      } catch (err) {
        // Ignore duplicate errors
      }
    }
    categories = await Category.findAll();
  }

  return categories;
}

/**
 * Check if a category exists by name.
 */
async function categoryExists(name) {
  const category = await Category.findByName(name);
  return !!category;
}

module.exports = {
  getAllCategories,
  categoryExists,
};
