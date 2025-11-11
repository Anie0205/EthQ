import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const login = async (email, password) => {
  const response = await axios.post(`${API_URL}/auth/token`, 
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
};

export const register = async (email, password) => {
  const response = await axios.post(`${API_URL}/auth/register`, { email, password });
  if (response.data.access_token) {
    localStorage.setItem('access_token', response.data.access_token);
  }
  return response.data;
};

export const logout = () => {
  localStorage.removeItem('access_token');
};

export const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return {
    Authorization: token ? `Bearer ${token}` : '',
  };
};
