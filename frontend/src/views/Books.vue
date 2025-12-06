<template>
  <main>
    <div class="container">
      <div class="content-header">
        <h1>Библиотека книг</h1>
        <div class="content-meta">Доступные произведения</div>
      </div>
      
      <div v-if="loading" class="loading">Загрузка книг...</div>
      
      <div v-else-if="error" class="error-message">
        {{ error }}
        <button @click="fetchBooks" class="btn">Повторить</button>
      </div>
      
      <div v-else class="books-container">
        <div v-if="books.length === 0" class="empty-state">
          <p>Библиотека пуста</p>
          <p>Войдите в систему, чтобы добавить книги</p>
        </div>
        
        <div v-else class="books-grid">
          <div v-for="book in books" :key="book.id" class="book-card">
            <!-- Контейнер для обложки книги -->
            <div class="book-cover-container">
              <img :src="getBookImage(book.id)" class="book-cover"/>
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
        if (err.response?.status === 401) {
          localStorage.removeItem('access_token')
          router.push('/auth')
          return
        }
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
.loading {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 18px;
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