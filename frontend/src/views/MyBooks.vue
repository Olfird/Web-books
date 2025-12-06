<template>
  <main>
    <div class="container">
      <div class="content-header">
        <h1>Мои книги</h1>
        <div class="content-meta">Книги в вашей личной коллекции</div>
      </div>
      
      <div class="user-info card" v-if="userProfile">
        <h3>Информация о профиле</h3>
        <p><strong>Имя пользователя:</strong> {{ userProfile.username }}</p>
        <p><strong>Всего книг в коллекции:</strong> {{ books.length }}</p>
      </div>

      <div v-if="loading" class="loading">Загрузка ваших книг...</div>

      <div v-else-if="error" class="error-message">
        {{ error }}
        <button @click="fetchMyBooks" class="btn">Повторить</button>
      </div>

      <div v-else-if="books.length === 0" class="empty-state">
        <p>У вас пока нет добавленных книг</p>
        <p>Перейдите в библиотеку, чтобы добавить книги в ваш профиль</p>
        <router-link to="/books" class="btn">Перейти в библиотеку</router-link>
      </div>
      
      <div v-else class="books-grid">
        <div v-for="userBook in books" class="book-card">
          <!-- Контейнер для обложки книги -->
          <div class="book-cover-container">
            <img :src="getBookImage(userBook)" class="book-cover"/>
          </div>
            
          <!-- Информация о книге -->
          <div class="book-info">
            <h3>{{ userBook.book?.title}}</h3>
            <p class="book-author">
              <strong>Автор:</strong> {{ userBook.book?.author}}
            </p>
            <p v-if="userBook.book?.year" class="book-year">
              <strong>Год:</strong> {{ userBook.book.year }}
            </p>
            <p class="added-date" v-if="userBook.added_at">
              <strong>Добавлено:</strong> {{ formatDate(userBook.added_at) }}
            </p>
          </div>

          <!-- Кнопки действий -->
          <div class="book-actions">
            <button
              @click="removeFromMyBooks(userBook.book_id)"
              class="btn-danger"
              :disabled="removingBooks.includes(userBook.book_id)"
            >
              {{ removingBooks.includes(userBook.book_id) ? 'Удаление...' : 'Удалить из коллекции' }}
            </button>
          </div>
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

    const getBookImage = (userBook) => {
      return `http://localhost:8000/static/books/${userBook.book_id}.jpg`
      }
      
    const formatDate = (dateString) => {
      try {
        const date = new Date(dateString)
        return date.toLocaleDateString('ru-RU', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
        })
      } catch {
        return dateString
      }
    }

    const handleImageError = (event) => {
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

        if (err.response?.status === 401) {
          localStorage.removeItem('access_token')
          router.push('/auth')
          return
        }
      } finally {
        loading.value = false
      }
    }

    const removeFromMyBooks = async (bookId) => {
      removingBooks.value.push(bookId)
      
      try {
        await usersAPI.removeBookFromProfile(bookId)
        
        books.value = books.value.filter(userBook => userBook.book_id !== bookId)
        
      } catch (err) {   
        if (err.response?.status === 401) {
          localStorage.removeItem('access_token')
          router.push('/auth')
          return
        }

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
      formatDate,
      handleImageError,
      fetchMyBooks,
      removeFromMyBooks
    }
  }
}
</script>

<style scoped>

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
  color: black;
  margin-bottom: 15px;
}

</style>