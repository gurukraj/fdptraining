const { body, query, param, validationResult } = require('express-validator');
const config = require('../config');
const { errorResponse } = require('../utils/helpers');

/**
 * Middleware to handle validation results.
 */
function handleValidationErrors(req, res, next) {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(422).json(errorResponse('Validation failed', errors.array()));
  }
  next();
}

/**
 * Validation rules for creating a product.
 */
const createProductRules = [
  body('name')
    .trim()
    .isLength({ min: config.validation.nameMinLength, max: config.validation.nameMaxLength })
    .withMessage(`Name must be between ${config.validation.nameMinLength} and ${config.validation.nameMaxLength} characters`),
  body('price')
    .isFloat({ gt: 0 })
    .withMessage('Price must be a positive number')
    .custom((value) => {
      const decimals = value.toString().split('.')[1];
      if (decimals && decimals.length > config.validation.maxPriceDecimals) {
        throw new Error(`Price can have at most ${config.validation.maxPriceDecimals} decimal places`);
      }
      return true;
    }),
  body('category')
    .trim()
    .notEmpty()
    .withMessage('Category is required')
    .custom((value) => {
      const found = config.validCategories.some(
        (c) => c.toLowerCase() === value.toLowerCase()
      );
      if (!found) {
        throw new Error(`Category must be one of: ${config.validCategories.join(', ')}`);
      }
      return true;
    }),
  body('description')
    .optional()
    .trim()
    .isLength({ max: config.validation.descriptionMaxLength })
    .withMessage(`Description can be at most ${config.validation.descriptionMaxLength} characters`),
  body('tags')
    .optional()
    .isArray({ max: config.validation.maxTags })
    .withMessage(`Tags must be an array with at most ${config.validation.maxTags} items`),
  body('tags.*')
    .optional()
    .trim()
    .isLength({ min: config.validation.tagMinLength, max: config.validation.tagMaxLength })
    .withMessage(`Each tag must be between ${config.validation.tagMinLength} and ${config.validation.tagMaxLength} characters`),
  body('imageUrl')
    .optional()
    .trim()
    .isURL()
    .withMessage('Image URL must be a valid URL'),
  body('stock')
    .optional()
    .isInt({ min: 0 })
    .withMessage('Stock must be a non-negative integer'),
  handleValidationErrors,
];

/**
 * Validation rules for updating a product.
 */
const updateProductRules = [
  param('id').notEmpty().withMessage('Product ID is required'),
  body('name')
    .optional()
    .trim()
    .isLength({ min: config.validation.nameMinLength, max: config.validation.nameMaxLength })
    .withMessage(`Name must be between ${config.validation.nameMinLength} and ${config.validation.nameMaxLength} characters`),
  body('price')
    .optional()
    .isFloat({ gt: 0 })
    .withMessage('Price must be a positive number')
    .custom((value) => {
      const decimals = value.toString().split('.')[1];
      if (decimals && decimals.length > config.validation.maxPriceDecimals) {
        throw new Error(`Price can have at most ${config.validation.maxPriceDecimals} decimal places`);
      }
      return true;
    }),
  body('category')
    .optional()
    .trim()
    .custom((value) => {
      const found = config.validCategories.some(
        (c) => c.toLowerCase() === value.toLowerCase()
      );
      if (!found) {
        throw new Error(`Category must be one of: ${config.validCategories.join(', ')}`);
      }
      return true;
    }),
  body('description')
    .optional()
    .trim()
    .isLength({ max: config.validation.descriptionMaxLength })
    .withMessage(`Description can be at most ${config.validation.descriptionMaxLength} characters`),
  body('tags')
    .optional()
    .isArray({ max: config.validation.maxTags })
    .withMessage(`Tags must be an array with at most ${config.validation.maxTags} items`),
  body('tags.*')
    .optional()
    .trim()
    .isLength({ min: config.validation.tagMinLength, max: config.validation.tagMaxLength })
    .withMessage(`Each tag must be between ${config.validation.tagMinLength} and ${config.validation.tagMaxLength} characters`),
  body('imageUrl')
    .optional()
    .trim()
    .isURL()
    .withMessage('Image URL must be a valid URL'),
  body('stock')
    .optional()
    .isInt({ min: 0 })
    .withMessage('Stock must be a non-negative integer'),
  body('viewCount')
    .not()
    .exists()
    .withMessage('viewCount cannot be updated via this endpoint'),
  body('isDeleted')
    .not()
    .exists()
    .withMessage('isDeleted cannot be updated via this endpoint'),
  handleValidationErrors,
];

/**
 * Validation rules for stock adjustment.
 */
const stockAdjustmentRules = [
  param('id').notEmpty().withMessage('Product ID is required'),
  body('adjustment')
    .isInt()
    .withMessage('Adjustment must be an integer'),
  handleValidationErrors,
];

/**
 * Validation rules for listing/searching products.
 */
const listProductRules = [
  query('page')
    .optional()
    .isInt({ min: 1 })
    .withMessage('Page must be a positive integer'),
  query('limit')
    .optional()
    .isInt({ min: 1, max: config.pagination.maxLimit })
    .withMessage(`Limit must be between 1 and ${config.pagination.maxLimit}`),
  query('sortBy')
    .optional()
    .isIn(['price', 'name', 'createdAt', 'viewCount'])
    .withMessage('sortBy must be one of: price, name, createdAt, viewCount'),
  query('sortOrder')
    .optional()
    .isIn(['asc', 'desc'])
    .withMessage('sortOrder must be asc or desc'),
  query('minPrice')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('minPrice must be a non-negative number'),
  query('maxPrice')
    .optional()
    .isFloat({ min: 0 })
    .withMessage('maxPrice must be a non-negative number'),
  handleValidationErrors,
];

module.exports = {
  handleValidationErrors,
  createProductRules,
  updateProductRules,
  stockAdjustmentRules,
  listProductRules,
};
