const Datastore = require('nedb-promises');
const path = require('path');
const config = require('../config');

let db;

function getDb() {
  if (!db) {
    db = Datastore.create({
      filename: config.db.productsPath,
      autoload: true,
    });

    // Add indexes for common query fields
    db.ensureIndex({ fieldName: 'name' });
    db.ensureIndex({ fieldName: 'category' });
    db.ensureIndex({ fieldName: 'isDeleted' });
    db.ensureIndex({ fieldName: 'price' });
    db.ensureIndex({ fieldName: 'viewCount' });
  }
  return db;
}

/**
 * Product Model - wraps nedb-promises with MongoDB-like interface
 */
const Product = {
  /**
   * Get the underlying datastore (useful for testing).
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
   * Create a new product.
   * @param {object} productData
   * @returns {Promise<object>}
   */
  async create(productData) {
    const now = new Date().toISOString();
    const product = {
      ...productData,
      viewCount: 0,
      priceHistory: [],
      isDeleted: false,
      deletedAt: null,
      createdAt: now,
      updatedAt: now,
    };
    return getDb().insert(product);
  },

  /**
   * Find a product by ID.
   * @param {string} id
   * @returns {Promise<object|null>}
   */
  async findById(id) {
    return getDb().findOne({ _id: id });
  },

  /**
   * Find products with query, sort, skip, limit.
   * @param {object} query
   * @param {object} sort
   * @param {number} skip
   * @param {number} limit
   * @returns {Promise<object[]>}
   */
  async find(query = {}, sort = { createdAt: -1 }, skip = 0, limit = 10) {
    return getDb().find(query).sort(sort).skip(skip).limit(limit);
  },

  /**
   * Count documents matching query.
   * @param {object} query
   * @returns {Promise<number>}
   */
  async count(query = {}) {
    return getDb().count(query);
  },

  /**
   * Update a product by ID.
   * @param {string} id
   * @param {object} updateData
   * @returns {Promise<number>}
   */
  async updateById(id, updateData) {
    updateData.updatedAt = new Date().toISOString();
    return getDb().update({ _id: id }, { $set: updateData }, { returnUpdatedDocs: true });
  },

  /**
   * Push to an array field.
   * @param {string} id
   * @param {string} field
   * @param {*} value
   * @returns {Promise<number>}
   */
  async pushToArray(id, field, value) {
    return getDb().update(
      { _id: id },
      {
        $push: { [field]: value },
        $set: { updatedAt: new Date().toISOString() },
      }
    );
  },

  /**
   * Increment a numeric field.
   * @param {string} id
   * @param {string} field
   * @param {number} value
   * @returns {Promise<number>}
   */
  async increment(id, field, value = 1) {
    return getDb().update(
      { _id: id },
      {
        $set: { updatedAt: new Date().toISOString() },
      }
    );
  },

  /**
   * Find all non-deleted products (for analytics).
   * @param {object} query
   * @returns {Promise<object[]>}
   */
  async findAll(query = {}) {
    return getDb().find(query);
  },

  /**
   * Remove all documents (for testing).
   * @returns {Promise<number>}
   */
  async removeAll() {
    return getDb().remove({}, { multi: true });
  },
};

module.exports = Product;
