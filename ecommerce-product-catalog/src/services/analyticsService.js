const Product = require('../models/Product');

/**
 * Get most viewed products.
 * @param {number} limit - Number of products to return (default 10)
 */
async function getMostViewed(limit = 10) {
  const limitNum = parseInt(limit, 10) || 10;
  const products = await Product.find(
    { isDeleted: false },
    { viewCount: -1 },
    0,
    limitNum
  );
  return products;
}

/**
 * Get category breakdown - count and average price per category.
 */
async function getCategoryBreakdown() {
  const products = await Product.findAll({ isDeleted: false });

  const categoryMap = {};
  for (const product of products) {
    const cat = product.category;
    if (!categoryMap[cat]) {
      categoryMap[cat] = { category: cat, count: 0, totalPrice: 0 };
    }
    categoryMap[cat].count += 1;
    categoryMap[cat].totalPrice += product.price;
  }

  const breakdown = Object.values(categoryMap).map((entry) => ({
    category: entry.category,
    count: entry.count,
    averagePrice: Math.round((entry.totalPrice / entry.count) * 100) / 100,
  }));

  // Sort by count descending
  breakdown.sort((a, b) => b.count - a.count);

  return breakdown;
}

/**
 * Get price distribution stats across all active products.
 */
async function getPriceDistribution() {
  const products = await Product.findAll({ isDeleted: false });

  if (products.length === 0) {
    return {
      totalProducts: 0,
      min: 0,
      max: 0,
      average: 0,
      median: 0,
    };
  }

  const prices = products.map((p) => p.price).sort((a, b) => a - b);
  const total = prices.reduce((sum, p) => sum + p, 0);
  const avg = Math.round((total / prices.length) * 100) / 100;

  // Calculate median
  let median;
  const mid = Math.floor(prices.length / 2);
  if (prices.length % 2 === 0) {
    median = Math.round(((prices[mid - 1] + prices[mid]) / 2) * 100) / 100;
  } else {
    median = prices[mid];
  }

  return {
    totalProducts: products.length,
    min: prices[0],
    max: prices[prices.length - 1],
    average: avg,
    median,
  };
}

module.exports = {
  getMostViewed,
  getCategoryBreakdown,
  getPriceDistribution,
};
