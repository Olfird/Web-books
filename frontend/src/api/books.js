import apiClient from './index'

export const booksApi = {
  // Получение всех книг из каталога
  getAllBooks() {
    return apiClient.get('/books_catalog/')
  },

  // Получение одной книги по ID
  getBookById(id) {
    return apiClient.get(`/books_catalog/${id}`)
  },

  // Добавление новой книги в каталог (если нужно админом)
  addBook(bookData) {
    return apiClient.post('/books_catalog/', bookData)
  }
}