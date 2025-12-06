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

  uploadBookImage(bookId, imageFile) {
    const formData = new FormData();
    formData.append('file', imageFile);
    
    return api.post(`/books_catalog/${bookId}/upload-image`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

};