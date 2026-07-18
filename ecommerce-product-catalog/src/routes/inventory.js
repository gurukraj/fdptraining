const express = require('express');
const router = express.Router();
const inventoryService = require('../services/inventoryService');
const { stockAdjustmentRules } = require('../middleware/validator');
const { successResponse } = require('../utils/helpers');

/**
 * PATCH /api/products/:id/stock - Adjust product stock
 */
router.patch('/:id/stock', stockAdjustmentRules, async (req, res, next) => {
  try {
    const result = await inventoryService.adjustStock(req.params.id, req.body.adjustment);
    res.json(successResponse(result));
  } catch (err) {
    next(err);
  }
});

/**
 * GET /api/products/inventory/low-stock - Get low stock products
 */
router.get('/inventory/low-stock', async (req, res, next) => {
  try {
    const { threshold = 10, page, limit } = req.query;
    const { products, pagination } = await inventoryService.getLowStockProducts(threshold, page, limit);
    res.json(successResponse(products, pagination));
  } catch (err) {
    next(err);
  }
});

module.exports = router;
