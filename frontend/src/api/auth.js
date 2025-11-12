// frontend/src/api/auth.js
import axios from 'axios';
import { API_BASE_URL } from './config';

const API_URL = API_BASE_URL;

// Add request interceptor for debugging
axios.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    console.log('Headers:', config.headers);
    console.log('Has Auth Token:', !!config.headers?.Authorization);
    return config;
  },
  (error) => {
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
axios.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    console.log('Response data:', response.data);
    return response;
  },
  (error) => {
    console.error('Response Error:', error.response?.status, error.message);
    console.error('Error response data:', error.response?.data);
    console.error('Error response headers:', error.response?.headers);
    return Promise.reject(error);
  }
);

export const login = async (email, password) => {
  try {
    const response = await axios.post(
      `${API_URL}/token`,  // Changed from /auth/token
      new URLSearchParams({
        username: email,
        password: password,
      }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    );
    
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
    }
    
    return response.data;
  } catch (error) {
    console.error('Login error:', error.response?.data || error.message);
    throw error;
  }
};

export const register = async (email, password) => {
  try {
    const response = await axios.post(
      `${API_URL}/register`,  // Changed from /auth/register
      { email, password }
    );
    
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
    }
    
    return response.data;
  } catch (error) {
    console.error('Register error:', error.response?.data || error.message);
    throw error;
  }
};

export const logout = () => {
  localStorage.removeItem('access_token');
};

export const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  const headers = {};
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  return headers;
};