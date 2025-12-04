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
        <!-- Форма добавления книги -->
        <div v-if="isAuthenticated" class="card add-book-form">
          <h3>Добавить новую книгу</h3>
          <form @submit.prevent="addNewBook">
            <div class="form-group">
              <input 
                type="text" 
                v-model="newBook.title" 
                placeholder="Название книги" 
                required
              />
            </div>
            <div class="form-group">
              <input 
                type="text" 
                v-model="newBook.author" 
                placeholder="Автор" 
                required
              />
            </div>
            <div class="form-group">
              <input 
                type="number" 
                v-model="newBook.year" 
                placeholder="Год издания" 
                min="1000" 
                max="2024"
              />
            </div>
            <button type="submit" class="btn" :disabled="addingBook">
              {{ addingBook ? 'Добавление...' : 'Добавить книгу' }}
            </button>
          </form>
        </div>
        
        <div v-if="books.length === 0" class="empty-state">
          <p>📚 Библиотека пуста</p>
          <p v-if="isAuthenticated">Добавьте первую книгу!</p>
          <p v-else>Войдите в систему, чтобы добавить книги</p>
        </div>
        
        <div v-else class="books-grid">
          <div v-for="book in books" :key="book.id" class="book-card">
            <h3>{{ book.title }}</h3>
            <p><strong>Автор:</strong> {{ book.author }}</p>
            <p v-if="book.year"><strong>Год:</strong> {{ book.year }}</p>
            <p><strong>ID:</strong> {{ book.id }}</p>
            
            <div class="book-actions">
              <button 
                v-if="isAuthenticated && !isBookInMyCollection(book.id)" 
                @click="addToMyBooks(book.id)" 
                class="btn"
                :disabled="addingBooks.includes(book.id)"
              >
                {{ addingBooks.includes(book.id) ? 'Добавляется...' : 'Добавить в мои книги' }}
              </button>
              
              <span v-else-if="isAuthenticated && isBookInMyCollection(book.id)" class="added-badge">
                ✓ В вашей коллекции
              </span>
              
              <router-link v-else to="/auth" class="btn">
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
    const addingBook = ref(false)
    const addingBooks = ref([])
    const newBook = ref({
      title: '',
      author: '',
      year: ''
    })
    
    const myBooks = ref([])
    const isAuthenticated = computed(() => !!localStorage.getItem('access_token'))

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
        // Если ошибка 401, очищаем токен
        if (err.response?.status === 401) {
          localStorage.removeItem('access_token')
          window.location.reload()
        }
        myBooks.value = []
      }
    }

    // Добавляем новую книгу
    const addNewBook = async () => {
      if (!isAuthenticated.value) {
        router.push('/auth')
        return
      }
      
      addingBook.value = true
      
      try {
        const bookData = {
          title: newBook.value.title,
          author: newBook.value.author,
          year: newBook.value.year ? parseInt(newBook.value.year) : undefined
        }
        
        const response = await booksAPI.addBook(bookData)
        
        // Очищаем форму
        newBook.value = { title: '', author: '', year: '' }
        
        // Обновляем список книг
        await fetchBooks()
        
        // Добавляем книгу в коллекцию пользователя
        if (response.data.book_id) {
          await addToMyBooks(response.data.book_id)
        }
        
      } catch (err) {
        console.error('Failed to add book:', err)
        alert('Не удалось добавить книгу. Проверьте данные.')
      } finally {
        addingBook.value = false
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
        
        alert('Книга добавлена в вашу коллекцию!')
        
      } catch (err) {
        console.error('Failed to add book to profile:', err)
        
        // Если ошибка авторизации
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
      addingBook,
      addingBooks,
      newBook,
      myBooks,
      isAuthenticated,
      fetchBooks,
      addNewBook,
      addToMyBooks,
      isBookInMyCollection
    }
  }
}
</script>

<style scoped>
.add-book-form {
  margin-bottom: 30px;
  background-color: #f8f9fa;
}

.add-book-form h3 {
  margin-bottom: 20px;
  color: #2c3e50;
}

.book-actions {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.added-badge {
  display: inline-block;
  background-color: #27ae60;
  color: white;
  padding: 8px 15px;
  border-radius: 4px;
  font-size: 14px;
}
</style>