import api from './index.js';

export const booksAPI = {
  // Получить все книги
  getAllBooks() {
    return api.get('/books_catalog/');
  },

  // Получить конкретную книгу
  getBookById(bookId) {
    return api.get(`/books_catalog/${bookId}`);
  },

  // Добавить новую книгу
  addBook(bookData) {
    return api.post('/books_catalog/', bookData);
  },

  // Удалить книгу (если есть такой эндпоинт)
  deleteBook(bookId) {
    return api.delete(`/books_catalog/${bookId}`);
  },

  uploadBookImage(bookId, imageFile) {
    const formData = new FormData();
    formData.append('file', imageFile);
    
    return api.post(`/books_catalog/${bookId}/upload-image`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // Обновить книгу (если есть такой эндпоинт)
  updateBook(bookId, bookData) {
    return api.put(`/books_catalog/${bookId}`, bookData);
  }
};