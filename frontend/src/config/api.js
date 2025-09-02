import axios from 'axios';
import tokenService from '../services/tokenService';
import { API_CONFIG } from './constants';

// Create a base axios instance
const axiosInstance = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add the auth token
axiosInstance.interceptors.request.use(
  (config) => {
    const token = tokenService.getAccessToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    // Check if it's a 401 error and not a retry request
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const newAccessToken = await tokenService.refreshToken();
        // Update the header for the retried request
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
        // Retry the original request with the new token
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        // If refresh fails, the tokenService will handle logout/redirect.
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export const buildApiUrl = (endpoint) => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};

export const api = {
  get: (url, params) => axiosInstance.get(url, { params }),
  post: (url, data) => axiosInstance.post(url, data),
  put: (url, data) => axiosInstance.put(url, data),
  delete: (url) => axiosInstance.delete(url),
};