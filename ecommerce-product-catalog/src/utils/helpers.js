/**
 * Round a number to a specified number of decimal places.
 * @param {number} value
 * @param {number} decimals
 * @returns {number}
 */
function roundToDecimals(value, decimals = 2) {
  const factor = Math.pow(10, decimals);
  return Math.round(value * factor) / factor;
}

/**
 * Deduplicate an array of strings (case-insensitive, preserves first occurrence casing).
 * @param {string[]} arr
 * @returns {string[]}
 */
function deduplicateTags(arr) {
  if (!arr || !Array.isArray(arr)) return [];
  const seen = new Set();
  return arr.filter((item) => {
    const lower = item.toLowerCase().trim();
    if (seen.has(lower)) return false;
    seen.add(lower);
    return true;
  });
}

/**
 * Build a pagination response object.
 * @param {number} totalCount
 * @param {number} page
 * @param {number} limit
 * @returns {object}
 */
function buildPagination(totalCount, page, limit) {
  const totalPages = Math.ceil(totalCount / limit) || 1;
  return {
    totalCount,
    page,
    limit,
    totalPages,
    hasNextPage: page < totalPages,
    hasPrevPage: page > 1,
  };
}

/**
 * Create a success response object.
 * @param {*} data
 * @param {object} [pagination]
 * @returns {object}
 */
function successResponse(data, pagination) {
  const response = { success: true, data };
  if (pagination) {
    response.pagination = pagination;
  }
  return response;
}

/**
 * Create an error response object.
 * @param {string} message
 * @param {*} [errors]
 * @returns {object}
 */
function errorResponse(message, errors) {
  const response = { success: false, error: message };
  if (errors) {
    response.errors = errors;
  }
  return response;
}

/**
 * Check if a string is a valid URL.
 * @param {string} str
 * @returns {boolean}
 */
function isValidUrl(str) {
  try {
    new URL(str);
    return true;
  } catch {
    return false;
  }
}

/**
 * Count decimal places of a number.
 * @param {number} num
 * @returns {number}
 */
function countDecimals(num) {
  if (Math.floor(num) === num) return 0;
  const str = num.toString();
  if (str.indexOf('.') === -1) return 0;
  return str.split('.')[1].length;
}

module.exports = {
  roundToDecimals,
  deduplicateTags,
  buildPagination,
  successResponse,
  errorResponse,
  isValidUrl,
  countDecimals,
};
