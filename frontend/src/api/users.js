import apiClient from './index'

export const usersApi = {
  // Регистрация нового пользователя
  register(userData) {
    return apiClient.post('/users/', userData)
  },

  // Получение информации о текущем пользователе
  getCurrentUser() {
    return apiClient.get('/users/me')
  },

  // Добавление книги в профиль пользователя
  addBookToProfile(bookId) {
    return apiClient.post(`/users/me/books/${bookId}`)
  },

  // Удаление книги из профиля пользователя
  removeBookFromProfile(bookId) {
    return apiClient.delete(`/users/me/books/${bookId}`)
  }
}