import client from './client';

export const authApi = {
  login: (credentials) => client.post('/auth/login/json', credentials),
  register: (userData) => client.post('/auth/register', userData),
  getMe: () => client.get('/auth/me'),
  updateProfile: (profileData) => client.put('/auth/profile', profileData),
};

export default authApi;
