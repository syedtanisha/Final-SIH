import React, { createContext, useContext, useState, useEffect } from 'react';
import { authApi } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('statlearn_user');
    return saved ? JSON.parse(saved) : null;
  });
  const [token, setToken] = useState(() => localStorage.getItem('statlearn_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const savedToken = localStorage.getItem('statlearn_token');
      if (savedToken) {
        try {
          const res = await authApi.getMe();
          setUser(res.data);
          localStorage.setItem('statlearn_user', JSON.stringify(res.data));
        } catch (err) {
          console.error("Session verification error:", err);
          logout();
        }
      }
      setLoading(false);
    };
    initAuth();
  }, []);

  const login = async (email, password) => {
    const res = await authApi.login({ username: email, password });
    const { access_token } = res.data;
    localStorage.setItem('statlearn_token', access_token);
    setToken(access_token);

    // Fetch user details from /auth/me
    const meRes = await authApi.getMe();
    const userData = meRes.data;
    setUser(userData);
    localStorage.setItem('statlearn_user', JSON.stringify(userData));
    return userData;
  };

  const register = async (userData) => {
    await authApi.register(userData);
    return await login(userData.email, userData.password);
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    localStorage.removeItem('statlearn_token');
    localStorage.removeItem('statlearn_user');
  };

  const refreshUser = async () => {
    try {
      const res = await authApi.getMe();
      setUser(res.data);
      localStorage.setItem('statlearn_user', JSON.stringify(res.data));
    } catch (err) {
      console.error("Error refreshing user:", err);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!token,
        isAdmin: user?.role === 'admin',
        loading,
        login,
        register,
        logout,
        refreshUser,
      }}
    >
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
