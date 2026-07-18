const express = require('express');
const router = express.Router();
const categoryService = require('../services/categoryService');
const { successResponse } = require('../utils/helpers');

/**
 * GET /api/categories - List all categories
 */
router.get('/', async (req, res, next) => {
  try {
    const categories = await categoryService.getAllCategories();
    res.json(successResponse(categories));
  } catch (err) {
    next(err);
  }
});

module.exports = router;
