const { errorResponse } = require('../utils/helpers');

/**
 * Custom application error class.
 */
class AppError extends Error {
  constructor(message, statusCode = 500) {
    super(message);
    this.statusCode = statusCode;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

/**
 * Not Found middleware - catches unmatched routes.
 */
function notFoundHandler(req, res, next) {
  const err = new AppError(`Route not found: ${req.method} ${req.originalUrl}`, 404);
  next(err);
}

/**
 * Global error handler middleware.
 */
function globalErrorHandler(err, req, res, _next) {
  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';

  if (process.env.NODE_ENV !== 'test') {
    console.error(`[ERROR] ${statusCode} - ${message}`);
    if (statusCode === 500) {
      console.error(err.stack);
    }
  }

  res.status(statusCode).json(errorResponse(message));
}

module.exports = {
  AppError,
  notFoundHandler,
  globalErrorHandler,
};
