const Product = require('../models/Product');
const config = require('../config');
const { AppError } = require('../middleware/errorHandler');
const { deduplicateTags, buildPagination } = require('../utils/helpers');

/**
 * Create a new product.
 */
async function createProduct(data) {
  // Normalize category casing to match valid categories
  const normalizedCategory = config.validCategories.find(
    (c) => c.toLowerCase() === data.category.toLowerCase()
  );
  if (!normalizedCategory) {
    throw new AppError(`Invalid category: ${data.category}`, 400);
  }

  // Check for duplicate name + category
  const existing = await Product.find({
    name: data.name,
    category: normalizedCategory,
    isDeleted: false,
  });
  if (existing.length > 0) {
    throw new AppError('A product with this name already exists in this category', 409);
  }

  // Prepare product data
  const productData = {
    name: data.name,
    description: data.description || '',
    price: data.price,
    category: normalizedCategory,
    tags: deduplicateTags(data.tags || []),
    imageUrl: data.imageUrl || null,
    stock: data.stock !== undefined ? data.stock : 0,
  };

  return Product.create(productData);
}

/**
 * List products with search, filter, sort, and pagination.
 */
async function listProducts(queryParams) {
  const {
    search,
    category,
    minPrice,
    maxPrice,
    tags,
    page = config.pagination.defaultPage,
    limit = config.pagination.defaultLimit,
    sortBy = 'createdAt',
    sortOrder = 'desc',
  } = queryParams;

  const pageNum = parseInt(page, 10) || config.pagination.defaultPage;
  const limitNum = Math.min(parseInt(limit, 10) || config.pagination.defaultLimit, config.pagination.maxLimit);

  // Build query - always exclude soft-deleted products
  const query = { isDeleted: false };

  // Full-text search across name and description
  if (search) {
    const searchRegex = new RegExp(escapeRegex(search), 'i');
    query.$or = [
      { name: searchRegex },
      { description: searchRegex },
    ];
  }

  // Category filter (case-insensitive)
  if (category) {
    query.category = new RegExp(`^${escapeRegex(category)}$`, 'i');
  }

  // Price range filters
  if (minPrice !== undefined || maxPrice !== undefined) {
    query.price = {};
    if (minPrice !== undefined) query.price.$gte = parseFloat(minPrice);
    if (maxPrice !== undefined) query.price.$lte = parseFloat(maxPrice);
  }

  // Tags filter (ANY match)
  if (tags) {
    const tagList = tags.split(',').map((t) => t.trim().toLowerCase());
    // nedb doesn't have $elemMatch with regex well, so we'll filter in memory
    // For the query, we'll use a broader approach
    query._tagsFilter = tagList; // custom marker, handled below
  }

  // Remove custom markers before querying
  const tagsFilter = query._tagsFilter;
  delete query._tagsFilter;

  // Build sort object
  const sort = {};
  sort[sortBy] = sortOrder === 'asc' ? 1 : -1;

  // Get total count and paginated results
  let totalCount;
  let products;

  if (tagsFilter) {
    // For tags filtering, we need to get all matching docs and filter in memory
    const allProducts = await Product.findAll(query);
    const filtered = allProducts.filter((p) =>
      p.tags && p.tags.some((tag) => tagsFilter.includes(tag.toLowerCase()))
    );
    totalCount = filtered.length;

    // Sort in memory
    filtered.sort((a, b) => {
      const aVal = a[sortBy];
      const bVal = b[sortBy];
      if (aVal < bVal) return sortOrder === 'asc' ? -1 : 1;
      if (aVal > bVal) return sortOrder === 'asc' ? 1 : -1;
      return 0;
    });

    // Paginate in memory
    const skip = (pageNum - 1) * limitNum;
    products = filtered.slice(skip, skip + limitNum);
  } else {
    totalCount = await Product.count(query);
    const skip = (pageNum - 1) * limitNum;
    products = await Product.find(query, sort, skip, limitNum);
  }

  const pagination = buildPagination(totalCount, pageNum, limitNum);
  return { products, pagination };
}

/**
 * Get a single product by ID and increment view count.
 */
async function getProductById(id, incrementView = true) {
  const product = await Product.findById(id);
  if (!product) {
    throw new AppError('Product not found', 404);
  }
  if (product.isDeleted) {
    throw new AppError('Product not found', 404);
  }

  if (incrementView) {
    // Increment view count
    const newViewCount = (product.viewCount || 0) + 1;
    await Product.updateById(id, { viewCount: newViewCount });
    product.viewCount = newViewCount;
  }

  return product;
}

/**
 * Update a product by ID (partial update).
 */
async function updateProduct(id, data) {
  const product = await Product.findById(id);
  if (!product) {
    throw new AppError('Product not found', 404);
  }
  if (product.isDeleted) {
    throw new AppError('Product not found', 404);
  }

  // Build update object with only provided fields
  const updateData = {};

  if (data.name !== undefined) updateData.name = data.name;
  if (data.description !== undefined) updateData.description = data.description;
  if (data.category !== undefined) {
    const normalizedCategory = config.validCategories.find(
      (c) => c.toLowerCase() === data.category.toLowerCase()
    );
    if (!normalizedCategory) {
      throw new AppError(`Invalid category: ${data.category}`, 400);
    }
    updateData.category = normalizedCategory;
  }
  if (data.tags !== undefined) updateData.tags = deduplicateTags(data.tags);
  if (data.imageUrl !== undefined) updateData.imageUrl = data.imageUrl;
  if (data.stock !== undefined) updateData.stock = data.stock;

  // Track price changes
  if (data.price !== undefined && data.price !== product.price) {
    updateData.price = data.price;
    // Push to price history
    await Product.pushToArray(id, 'priceHistory', {
      oldPrice: product.price,
      newPrice: data.price,
      changedAt: new Date().toISOString(),
    });
  }

  // Check for duplicate name+category if name or category changed
  if (updateData.name || updateData.category) {
    const checkName = updateData.name || product.name;
    const checkCategory = updateData.category || product.category;
    const duplicates = await Product.find({
      name: checkName,
      category: checkCategory,
      isDeleted: false,
    });
    const hasDuplicate = duplicates.some((p) => p._id !== id);
    if (hasDuplicate) {
      throw new AppError('A product with this name already exists in this category', 409);
    }
  }

  if (Object.keys(updateData).length === 0) {
    return product;
  }

  await Product.updateById(id, updateData);
  return Product.findById(id);
}

/**
 * Soft delete a product.
 */
async function deleteProduct(id) {
  const product = await Product.findById(id);
  if (!product) {
    throw new AppError('Product not found', 404);
  }
  if (product.isDeleted) {
    throw new AppError('Product is already deleted', 400);
  }

  await Product.updateById(id, {
    isDeleted: true,
    deletedAt: new Date().toISOString(),
  });

  return { message: 'Product soft-deleted successfully' };
}

/**
 * Restore a soft-deleted product.
 */
async function restoreProduct(id) {
  const product = await Product.findById(id);
  if (!product) {
    throw new AppError('Product not found', 404);
  }
  if (!product.isDeleted) {
    throw new AppError('Product is not deleted', 400);
  }

  await Product.updateById(id, {
    isDeleted: false,
    deletedAt: null,
  });

  return { message: 'Product restored successfully' };
}

/**
 * Escape special regex characters.
 */
function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

module.exports = {
  createProduct,
  listProducts,
  getProductById,
  updateProduct,
  deleteProduct,
  restoreProduct,
};
