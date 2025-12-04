<template>
  <main>
    <div class="container">
      <div class="my-books-container">
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
          <div v-for="book in books" :key="book.id" class="book-card">
            <h3>{{ book.title }}</h3>
            <p><strong>Автор:</strong> {{ book.author }}</p>
            <p v-if="book.year"><strong>Год:</strong> {{ book.year }}</p>
            
            <div class="book-actions">
              <button 
                @click="removeFromMyBooks(book.id)" 
                class="btn btn-danger"
                :disabled="removingBooks.includes(book.id)"
              >
                {{ removingBooks.includes(book.id) ? 'Удаление...' : 'Удалить из коллекции' }}
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

    // Загружаем книги пользователя
    const fetchMyBooks = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const response = await usersAPI.getProfile()
        userProfile.value = response.data
        books.value = response.data.user_books || []
      } catch (err) {
        console.error('Failed to fetch user books:', err)
        
        // Если ошибка 401, очищаем токен и перенаправляем
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

    // Удаляем книгу из коллекции
    const removeFromMyBooks = async (bookId) => {
      if (!confirm('Вы уверены, что хотите удалить эту книгу из своей коллекции?')) {
        return
      }
      
      removingBooks.value.push(bookId)
      
      try {
        await usersAPI.removeBookFromProfile(bookId)
        
        // Удаляем книгу из локального списка
        books.value = books.value.filter(book => book.id !== bookId)
        
        // Обновляем профиль
        if (userProfile.value) {
          userProfile.value.user_books = books.value
        }
        
        alert('Книга удалена из вашей коллекции')
        
      } catch (err) {
        console.error('Failed to remove book:', err)
        
        // Если ошибка авторизации
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
      // Проверяем авторизацию перед загрузкой
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
      fetchMyBooks,
      removeFromMyBooks
    }
  }
}
</script>

<style scoped>
.user-info {
  margin-top: 40px;
  background-color: #f8f9fa;
}

.user-info h3 {
  margin-bottom: 15px;
  color: #2c3e50;
}

.user-info p {
  margin: 8px 0;
}

.btn-danger {
  background-color: #e74c3c;
}

.btn-danger:hover {
  background-color: #c0392b;
}
</style>