<template>
  <main>
    <div class="container">
      <div class="content-header">
        <h1>Библиотека книг</h1>
        <div class="content-meta">Доступные для чтения произведения</div>
      </div>
      
      <div v-if="loading" class="loading">Загрузка книг...</div>
      
      <div v-else-if="error" class="error-message">
        {{ error }}
        <button @click="fetchBooks" class="btn">Повторить</button>
      </div>
      
      <div v-else class="books-container">
        <div v-if="books.length === 0" class="empty-state">
          <p>📚 Библиотека пуста</p>
          <p>Войдите в систему, чтобы добавить книги</p>
        </div>
        
        <div v-else class="books-grid">
          <div v-for="book in books" :key="book.id" class="book-card">
            <!-- Контейнер для обложки книги -->
            <div class="book-cover-container">
              <img 
                :src="getBookImage(book.id)" 
                class="book-cover"
                :alt="book.title"
                @error="handleImageError"
              />
            </div>

            <div class="book-info">
              <h3>{{ book.title }}</h3>
              <p class="book-author"><strong>Автор:</strong> {{ book.author }}</p>
              <p v-if="book.year" class="book-year"><strong>Год:</strong> {{ book.year }}</p>
            </div>
            
            <div class="book-actions">
              <button 
                v-if="isAuthenticated && !isBookInMyCollection(book.id)" 
                @click="addToMyBooks(book.id)" 
                class="btn btn-add"
                :disabled="addingBooks.includes(book.id)"
              >
                {{ addingBooks.includes(book.id) ? 'Добавляется...' : 'Добавить в мои книги' }}
              </button>
              
              <span v-else-if="isAuthenticated && isBookInMyCollection(book.id)" class="added-badge">
                ✓ В вашей коллекции
              </span>
              
              <router-link v-else to="/auth" class="btn btn-login">
                Войдите, чтобы добавить
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { booksAPI } from '../api/books'
import { usersAPI } from '../api/users'

export default {
  name: 'BooksPage',
  setup() {
    const router = useRouter()
    
    const books = ref([])
    const loading = ref(true)
    const error = ref('')
    const addingBooks = ref([])
    
    const myBooks = ref([])
    const isAuthenticated = computed(() => !!localStorage.getItem('access_token'))

    const getBookImage = (bookId) => {
      return `http://localhost:8000/static/books/${bookId}.jpg`
    }

    const handleImageError = (event) => {
      console.log('Image failed to load:', event.target.src)
      event.target.style.display = 'none'
      event.target.parentElement.classList.add('no-image')
    }

    // Загружаем книги из каталога
    const fetchBooks = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const response = await booksAPI.getAllBooks()
        books.value = response.data
        
        // Загружаем книги пользователя только если авторизован
        if (isAuthenticated.value) {
          await fetchMyBooks()
        }
      } catch (err) {
        console.error('Failed to fetch books:', err)
        error.value = 'Не удалось загрузить книги. Попробуйте позже.'
      } finally {
        loading.value = false
      }
    }

    // Загружаем книги пользователя
    const fetchMyBooks = async () => {
      if (!isAuthenticated.value) {
        myBooks.value = []
        return
      }
      
      try {
        const response = await usersAPI.getProfile()
        myBooks.value = response.data.user_books || []
      } catch (err) {
        console.error('Failed to fetch user books:', err)
        if (err.response?.status === 401) {
          localStorage.removeItem('access_token')
          window.location.reload()
        }
        myBooks.value = []
      }
    }

    // Добавляем книгу в коллекцию
    const addToMyBooks = async (bookId) => {
      if (!isAuthenticated.value) {
        router.push('/auth')
        return
      }
      
      addingBooks.value.push(bookId)
      
      try {
        await usersAPI.addBookToProfile(bookId)
        
        // Обновляем список книг пользователя
        await fetchMyBooks()
        
      } catch (err) {
        console.error('Failed to add book to profile:', err)
        
        if (err.response?.status === 401) {
          localStorage.removeItem('access_token')
          router.push('/auth')
          return
        }
        
        alert('Не удалось добавить книгу в коллекцию.')
      } finally {
        addingBooks.value = addingBooks.value.filter(id => id !== bookId)
      }
    }

    // Проверяем, есть ли книга в коллекции
    const isBookInMyCollection = (bookId) => {
      return myBooks.value.some(record => record.book_id === bookId)
    }

    onMounted(() => {
      fetchBooks()
    })

    return {
      books,
      loading,
      error,
      addingBooks,
      myBooks,
      isAuthenticated,
      getBookImage,
      handleImageError,
      fetchBooks,
      addToMyBooks,
      isBookInMyCollection
    }
  }
}
</script>

<style scoped>
/* Контейнер для обложки книги */
.book-cover-container {
  width: 100%;
  height: 300px; /* Высота для пропорций 1000×1498 */
  margin-bottom: 15px;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background: linear-gradient(145deg, #f8f9fa 0%, #e9ecef 100%);
}

.book-cover-container.no-image::before {
  content: "📚";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 48px;
  color: #adb5bd;
}

/* Сама обложка книги */
.book-cover {
  width: 100%;
  height: 100%;
  object-fit: contain; /* Меняем с cover на contain чтобы не обрезалось */
  object-position: center;
  transition: transform 0.3s ease;
}

.book-card:hover .book-cover {
  transform: scale(1.05);
}

/* Информация о книге */
.book-info {
  margin-bottom: 15px;
  flex-grow: 1;
}

.book-info h3 {
  color: #2c3e50;
  margin-bottom: 8px;
  font-size: 18px;
  line-height: 1.4;
  font-weight: 600;
  min-height: 50px;
}

.book-author {
  color: #666;
  font-size: 14px;
  margin-bottom: 5px;
  font-style: italic;
}

.book-year {
  color: #888;
  font-size: 13px;
}

/* Кнопки действий */
.book-actions {
  margin-top: auto;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.btn-add {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
  font-size: 14px;
  transition: background-color 0.3s;
  font-weight: 500;
}

.btn-add:hover:not(:disabled) {
  background-color: #2980b9;
  transform: translateY(-1px);
}

.btn-add:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-login {
  background-color: #95a5a6;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
  font-size: 14px;
  transition: background-color 0.3s;
  text-decoration: none;
  display: block;
  text-align: center;
  font-weight: 500;
}

.btn-login:hover {
  background-color: #7f8c8d;
  transform: translateY(-1px);
}

.added-badge {
  display: block;
  text-align: center;
  background-color: #27ae60;
  color: white;
  padding: 10px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
}

/* Сетка книг */
.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 25px;
  margin-top: 30px;
}

.book-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 18px;
}

.error-message {
  background-color: #ffeaea;
  color: #e74c3c;
  padding: 20px;
  border-radius: 8px;
  margin: 20px 0;
  text-align: center;
}

.error-message .btn {
  margin-top: 10px;
  background-color: #e74c3c;
}

.error-message .btn:hover {
  background-color: #c0392b;
}

.empty-state {
  text-align: center;
  padding: 60px 40px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  margin-top: 30px;
}

.empty-state p {
  color: #666;
  font-size: 18px;
  margin-bottom: 20px;
}

.empty-state p:first-child {
  font-size: 24px;
  color: #2c3e50;
  margin-bottom: 15px;
}

</style>