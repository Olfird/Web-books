import api from './index.js';

export const usersAPI = {
  // Получить профиль текущего пользователя
  getProfile() {
    return api.get('/users/me');
  },

  // Добавить книгу в профиль
  addBookToProfile(bookId) {
    return api.post(`/users/me/books/${bookId}`);
  },

  // Удалить книгу из профиля
  removeBookFromProfile(bookId) {
    return api.delete(`/users/me/books/${bookId}`);
  }
};