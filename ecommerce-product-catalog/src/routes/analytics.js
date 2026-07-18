const express = require('express');
const router = express.Router();
const analyticsService = require('../services/analyticsService');
const { successResponse } = require('../utils/helpers');

/**
 * GET /api/analytics/most-viewed - Get most viewed products
 */
router.get('/most-viewed', async (req, res, next) => {
  try {
    const { limit = 10 } = req.query;
    const products = await analyticsService.getMostViewed(limit);
    res.json(successResponse(products));
  } catch (err) {
    next(err);
  }
});

/**
 * GET /api/analytics/category-breakdown - Category stats
 */
router.get('/category-breakdown', async (req, res, next) => {
  try {
    const breakdown = await analyticsService.getCategoryBreakdown();
    res.json(successResponse(breakdown));
  } catch (err) {
    next(err);
  }
});

/**
 * GET /api/analytics/price-distribution - Price distribution stats
 */
router.get('/price-distribution', async (req, res, next) => {
  try {
    const distribution = await analyticsService.getPriceDistribution();
    res.json(successResponse(distribution));
  } catch (err) {
    next(err);
  }
});

module.exports = router;
