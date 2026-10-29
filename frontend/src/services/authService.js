import api from './api';

export const authService = {
  // Login: Returns { token, username, role, message }
  login: async (username, password) => {
    const response = await api.post('/api/auth/login', { username, password });
    return response.data;
  },

  // Register: Returns { token, username, role, message }
  register: async (userData) => {
    const response = await api.post('/api/auth/register', userData);
    return response.data;
  },

  // Validate JWT
  validateToken: async (token) => {
    const response = await api.get(`/api/auth/validate?token=${token}`);
    return response.data;
  }
};
