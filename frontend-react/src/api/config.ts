/**
 * api/config.ts
 * =============
 * API configuration and base URL
 */

// Get API base URL from environment or use default
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

// API endpoints
export const API_ENDPOINTS = {
  chat: {
    query: `${API_BASE_URL}/chat/query`,
    queryStream: `${API_BASE_URL}/chat/query/stream`,
    route: `${API_BASE_URL}/chat/route`,
  },
  schema: `${API_BASE_URL}/schema`,
} as const;
