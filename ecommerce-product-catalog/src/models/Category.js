const Datastore = require('nedb-promises');
const path = require('path');
const config = require('../config');

let db;

function getDb() {
  if (!db) {
    db = Datastore.create({
      filename: config.db.categoriesPath,
      autoload: true,
    });

    db.ensureIndex({ fieldName: 'name', unique: true });
  }
  return db;
}

/**
 * Category Model - wraps nedb-promises with MongoDB-like interface
 */
const Category = {
  /**
   * Get the underlying datastore.
   */
  getDb,

  /**
   * Reset the database reference (useful for testing).
   */
  resetDb() {
    db = null;
  },

  /**
   * Set a custom database instance (for testing).
   */
  setDb(customDb) {
    db = customDb;
  },

  /**
   * Create a new category.
   * @param {object} categoryData
   * @returns {Promise<object>}
   */
  async create(categoryData) {
    const now = new Date().toISOString();
    const category = {
      ...categoryData,
      createdAt: now,
      updatedAt: now,
    };
    return getDb().insert(category);
  },

  /**
   * Find all categories.
   * @returns {Promise<object[]>}
   */
  async findAll() {
    return getDb().find({}).sort({ name: 1 });
  },

  /**
   * Find a category by name (case-insensitive).
   * @param {string} name
   * @returns {Promise<object|null>}
   */
  async findByName(name) {
    return getDb().findOne({ name: new RegExp(`^${escapeRegex(name)}$`, 'i') });
  },

  /**
   * Find a category by ID.
   * @param {string} id
   * @returns {Promise<object|null>}
   */
  async findById(id) {
    return getDb().findOne({ _id: id });
  },

  /**
   * Count categories.
   * @returns {Promise<number>}
   */
  async count() {
    return getDb().count({});
  },

  /**
   * Remove all documents (for testing).
   * @returns {Promise<number>}
   */
  async removeAll() {
    return getDb().remove({}, { multi: true });
  },
};

/**
 * Escape special regex characters in a string.
 * @param {string} str
 * @returns {string}
 */
function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

module.exports = Category;
