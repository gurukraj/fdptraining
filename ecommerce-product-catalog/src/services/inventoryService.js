const Product = require('../models/Product');
const { AppError } = require('../middleware/errorHandler');
const { buildPagination } = require('../utils/helpers');

/**
 * Adjust stock for a product.
 * @param {string} id - Product ID
 * @param {number} adjustment - Positive or negative integer
 */
async function adjustStock(id, adjustment) {
  const product = await Product.findById(id);
  if (!product) {
    throw new AppError('Product not found', 404);
  }
  if (product.isDeleted) {
    throw new AppError('Product not found', 404);
  }

  const newStock = (product.stock || 0) + adjustment;
  if (newStock < 0) {
    throw new AppError(
      `Insufficient stock. Current stock: ${product.stock}, requested adjustment: ${adjustment}`,
      400
    );
  }

  await Product.updateById(id, { stock: newStock });

  return {
    message: 'Stock updated successfully',
    productId: id,
    previousStock: product.stock,
    adjustment,
    newStock,
  };
}

/**
 * Get products with low stock.
 * @param {number} threshold - Stock threshold (default 10)
 * @param {number} page
 * @param {number} limit
 */
async function getLowStockProducts(threshold = 10, page = 1, limit = 10) {
  const thresholdNum = parseInt(threshold, 10) || 10;
  const pageNum = parseInt(page, 10) || 1;
  const limitNum = parseInt(limit, 10) || 10;

  // nedb doesn't support $lte in a simple way across find+count efficiently,
  // so we fetch all and filter
  const allProducts = await Product.findAll({ isDeleted: false });
  const lowStock = allProducts
    .filter((p) => (p.stock || 0) <= thresholdNum)
    .sort((a, b) => (a.stock || 0) - (b.stock || 0));

  const totalCount = lowStock.length;
  const skip = (pageNum - 1) * limitNum;
  const products = lowStock.slice(skip, skip + limitNum);
  const pagination = buildPagination(totalCount, pageNum, limitNum);

  return { products, pagination };
}

module.exports = {
  adjustStock,
  getLowStockProducts,
};
