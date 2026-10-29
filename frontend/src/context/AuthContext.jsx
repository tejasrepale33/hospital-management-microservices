import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem('hospital_jwt_token'));
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('hospital_user');
    return saved ? JSON.parse(saved) : null;
  });
  const [loading, setLoading] = useState(true);

  // Normalize role string: e.g. "ROLE_PATIENT" -> "PATIENT"
  const normalizeRole = (role) => {
    if (!role) return 'PATIENT';
    return role.replace('ROLE_', '').toUpperCase();
  };

  useEffect(() => {
    const checkAuth = async () => {
      const storedToken = localStorage.getItem('hospital_jwt_token');
      const storedUser = localStorage.getItem('hospital_user');

      if (storedToken && storedUser) {
        try {
          const res = await authService.validateToken(storedToken);
          if (res && res.valid) {
            setToken(storedToken);
            setUser(JSON.parse(storedUser));
          } else {
            logout();
          }
        } catch {
          // If network is offline or token invalid, keep stored if valid format or logout
          setToken(storedToken);
          setUser(JSON.parse(storedUser));
        }
      } else {
        logout();
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  const login = async (username, password) => {
    const data = await authService.login(username, password);
    if (data.token) {
      const normRole = normalizeRole(data.role);
      const userData = { username: data.username, role: normRole, rawRole: data.role };

      localStorage.setItem('hospital_jwt_token', data.token);
      localStorage.setItem('hospital_user', JSON.stringify(userData));

      setToken(data.token);
      setUser(userData);
      return userData;
    }
    throw new Error(data.message || 'Login failed');
  };

  const register = async (userData) => {
    const data = await authService.register(userData);
    if (data.token) {
      const normRole = normalizeRole(data.role);
      const registeredUser = { username: data.username, role: normRole, rawRole: data.role };

      localStorage.setItem('hospital_jwt_token', data.token);
      localStorage.setItem('hospital_user', JSON.stringify(registeredUser));

      setToken(data.token);
      setUser(registeredUser);
      return registeredUser;
    }
    throw new Error(data.message || 'Registration failed');
  };

  const logout = () => {
    localStorage.removeItem('hospital_jwt_token');
    localStorage.removeItem('hospital_user');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ token, user, isAuthenticated: !!token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
