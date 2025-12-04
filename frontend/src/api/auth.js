import api from './index.js';

export const authAPI = {
  // Регистрация
  register(username, password) {
    return api.post('/auth/register', { username, password });
  },

  // Вход
  login(username, password) {
    return api.post('/auth/login', { username, password });
  },

  // Выход
  logout() {
    return api.post('/auth/logout');
  }
};