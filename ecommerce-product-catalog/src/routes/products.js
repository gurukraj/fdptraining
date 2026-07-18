const express = require('express');
const router = express.Router();
const productService = require('../services/productService');
const { createProductRules, updateProductRules, listProductRules } = require('../middleware/validator');
const { successResponse } = require('../utils/helpers');

/**
 * POST /api/products - Create a new product
 */
router.post('/', createProductRules, async (req, res, next) => {
  try {
    const product = await productService.createProduct(req.body);
    res.status(201).json(successResponse(product));
  } catch (err) {
    next(err);
  }
});

/**
 * GET /api/products - List and search products
 */
router.get('/', listProductRules, async (req, res, next) => {
  try {
    const { products, pagination } = await productService.listProducts(req.query);
    res.json(successResponse(products, pagination));
  } catch (err) {
    next(err);
  }
});

/**
 * GET /api/products/:id - Get a single product (increments viewCount)
 */
router.get('/:id', async (req, res, next) => {
  try {
    const product = await productService.getProductById(req.params.id);
    res.json(successResponse(product));
  } catch (err) {
    next(err);
  }
});

/**
 * PUT /api/products/:id - Update a product
 */
router.put('/:id', updateProductRules, async (req, res, next) => {
  try {
    const product = await productService.updateProduct(req.params.id, req.body);
    res.json(successResponse(product));
  } catch (err) {
    next(err);
  }
});

/**
 * DELETE /api/products/:id - Soft delete a product
 */
router.delete('/:id', async (req, res, next) => {
  try {
    const result = await productService.deleteProduct(req.params.id);
    res.json(successResponse(result));
  } catch (err) {
    next(err);
  }
});

/**
 * POST /api/products/:id/restore - Restore a soft-deleted product
 */
router.post('/:id/restore', async (req, res, next) => {
  try {
    const result = await productService.restoreProduct(req.params.id);
    res.json(successResponse(result));
  } catch (err) {
    next(err);
  }
});

module.exports = router;
