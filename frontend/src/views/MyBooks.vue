<template>
  <main>
    <div class="container">
      <div class="content-header">
        <h1>Мои книги</h1>
        <div class="content-meta">Книги в вашей личной коллекции</div>
      </div>

      <div v-if="loading" class="loading">Загрузка ваших книг...</div>

      <div v-else-if="error" class="error-message">
        {{ error }}
        <button @click="fetchMyBooks" class="btn">Повторить</button>
      </div>

      <div v-else-if="books.length === 0" class="empty-state">
        <p>📚 У вас пока нет добавленных книг</p>
        <p>Перейдите в библиотеку, чтобы добавить книги в ваш профиль</p>
        <router-link to="/books" class="btn">Перейти в библиотеку</router-link>
      </div>

      <div v-else class="books-grid">
        <div
          v-for="book in books"
          :key="book.book_id"
          class="book-card"
        >
          <!-- Контейнер для обложки книги -->
          <div class="book-cover-container">
            <img
              :src="getBookImage(book)"
              class="book-cover"
              :alt="book.title"
              @error="handleImageError"
            />
          </div>

          <!-- Информация о книге -->
          <div class="book-info">
            <h3>{{ book.title }}</h3>
            <p class="book-author"><strong>Автор:</strong> {{ book.author }}</p>
            <p v-if="book.year" class="book-year"><strong>Год:</strong> {{ book.year }}</p>
          </div>

          <!-- Кнопки действий -->
          <div class="book-actions">
            <button
              @click="removeFromMyBooks(book.book_id)"
              class="btn btn-danger"
              :disabled="removingBooks.includes(book.book_id)"
            >
              {{ removingBooks.includes(book.book_id) ? 'Удаление...' : 'Удалить из коллекции' }}
            </button>
          </div>
        </div>
      </div>

      <div class="user-info card" v-if="userProfile">
        <h3>Информация о профиле</h3>
        <p><strong>Имя пользователя:</strong> {{ userProfile.username }}</p>
        <p><strong>Активен:</strong> {{ userProfile.is_active ? 'Да' : 'Нет' }}</p>
        <p><strong>Всего книг в коллекции:</strong> {{ books.length }}</p>
      </div>
    </div>
  </main>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usersAPI } from '../api/users'

export default {
  name: 'MyBooksPage',
  setup() {
    const router = useRouter()
    
    const books = ref([])
    const userProfile = ref(null)
    const loading = ref(true)
    const error = ref('')
    const removingBooks = ref([])

    const getBookImage = (book) => {
      if (book.image_url) {
        return `http://localhost:8000${book.image_url}`
      }
      return `http://localhost:8000/static/books/${book.book_id}.jpg`
    }

    const handleImageError = (event) => {
      console.log('Image failed to load:', event.target.src)
      event.target.style.display = 'none'
      event.target.parentElement.classList.add('no-image')
    }
    
    const fetchMyBooks = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const response = await usersAPI.getProfile()
        userProfile.value = response.data
        books.value = response.data.user_books || []
      } catch (err) {
        console.error('Failed to fetch user books:', err)
        
        if (err.response?.status === 401) {
          localStorage.removeItem('access_token')
          router.push('/auth')
          return
        }
        
        error.value = 'Не удалось загрузить ваши книги. Попробуйте позже.'
      } finally {
        loading.value = false
      }
    }

    const removeFromMyBooks = async (bookId) => {
      if (!confirm('Вы уверены, что хотите удалить эту книгу из своей коллекции?')) {
        return
      }
      
      removingBooks.value.push(bookId)
      
      try {
        await usersAPI.removeBookFromProfile(bookId)
        
        books.value = books.value.filter(book => book.book_id !== bookId)
        
        if (userProfile.value) {
          userProfile.value.user_books = books.value
        }
        
        alert('Книга удалена из вашей коллекции')
        
      } catch (err) {
        console.error('Failed to remove book:', err)
        
        if (err.response?.status === 401) {
          localStorage.removeItem('access_token')
          router.push('/auth')
          return
        }
        
        alert('Не удалось удалить книгу. Попробуйте снова.')
      } finally {
        removingBooks.value = removingBooks.value.filter(id => id !== bookId)
      }
    }

    onMounted(() => {
      const token = localStorage.getItem('access_token')
      if (!token) {
        router.push('/auth')
        return
      }
      
      fetchMyBooks()
    })

    return {
      books,
      userProfile,
      loading,
      error,
      removingBooks,
      getBookImage,
      handleImageError,
      fetchMyBooks,
      removeFromMyBooks
    }
  }
}
</script>

<style scoped>
/* Контейнер для обложки книги */
.book-cover-container {
  width: 100%;
  height: 300px;
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
  object-fit: contain;
  object-position: center;
  transition: transform 0.3s ease;
}

.book-card:hover .book-cover {
  transform: scale(1.05);
}

/* Информация о книге - ВОТ ЗДЕСЬ НАХОДЯТСЯ НАЗВАНИЕ, АВТОР И ГОД */
.book-info {
  margin-bottom: 15px;
  flex-grow: 1;
}

.book-info h3 {
  color: #2c3e50;
  margin-bottom: 10px;
  font-size: 18px;
  line-height: 1.4;
  font-weight: 600;
  min-height: 50px;
}

.book-author {
  color: #666;
  font-size: 14px;
  margin-bottom: 5px;
}

.book-author strong {
  color: #555;
  font-weight: 600;
}

.book-year {
  color: #888;
  font-size: 13px;
  margin-bottom: 5px;
}

.book-year strong {
  color: #555;
  font-weight: 600;
}

/* Кнопки действий */
.book-actions {
  margin-top: auto;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.btn-danger {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
  font-size: 14px;
  transition: all 0.3s;
  font-weight: 500;
}

.btn-danger:hover:not(:disabled) {
  background-color: #c0392b;
  transform: translateY(-1px);
}

.btn-danger:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

/* Информация о пользователе */
.user-info {
  margin-top: 40px;
  padding: 25px;
  background: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

.user-info h3 {
  margin-bottom: 20px;
  color: #2c3e50;
  font-size: 20px;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
}

.user-info p {
  margin: 12px 0;
  color: #555;
  font-size: 16px;
}

.user-info strong {
  color: #2c3e50;
}

/* Общие стили */
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

.empty-state .btn {
  margin-top: 10px;
  display: inline-block;
  width: auto;
  padding: 12px 30px;
}

/* Кнопка для страницы пустого состояния */
.btn {
  display: inline-block;
  background-color: #3498db;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  text-decoration: none;
  font-size: 14px;
  transition: background-color 0.3s;
  text-align: center;
  font-weight: 500;
}

.btn:hover:not(:disabled) {
  background-color: #2980b9;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

</style>