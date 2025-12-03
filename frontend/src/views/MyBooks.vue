<template>
  <main>
    <div class="container">
      <div class="my-books-container">
        <h1>Мои книги</h1>
        
        <div v-if="loading" class="loading">Загрузка ваших книг...</div>
        
        <div v-else-if="error" class="error-message">
          {{ error }}
          <button @click="loadUserBooks" class="btn">Повторить</button>
        </div>
        
        <div v-else-if="books.length === 0" class="empty-state">
          <p>📚 У вас пока нет добавленных книг</p>
          <p>Перейдите в библиотеку, чтобы добавить книги в ваш профиль</p>
          <router-link to="/books" class="btn">Перейти в библиотеку</router-link>
        </div>
        
        <div v-else class="books-grid">
          <div v-for="item in books" :key="item.id" class="book-card">
            <h3>{{ item.book.title }}</h3>
            <p><strong>Автор:</strong> {{ item.book.author }}</p>
            <p><strong>Год:</strong> {{ item.book.year }}</p>
            <p><strong>Добавлено:</strong> {{ formatDate(item.added_at) }}</p>
            <button 
              @click="removeBook(item.book_id)" 
              class="btn btn-danger"
              :disabled="removingBookId === item.book_id"
            >
              {{ removingBookId === item.book_id ? 'Удаляется...' : 'Удалить из моего списка' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { usersApi } from '../api/users'

const router = useRouter()
const books = ref([])
const loading = ref(false)
const error = ref('')
const removingBookId = ref(null)

// Загружаем книги пользователя
const loadUserBooks = async () => {
  try {
    loading.value = true
    error.value = ''
    const response = await usersApi.getCurrentUser()
    books.value = response.data.user_books || []
  } catch (err) {
    console.error('Ошибка загрузки книг:', err)
    
    if (err.response?.status === 401) {
      error.value = 'Вы не авторизованы. Пожалуйста, войдите в систему.'
      router.push('/auth')
    } else {
      error.value = 'Не удалось загрузить ваши книги'
    }
  } finally {
    loading.value = false
  }
}

// Удаляем книгу
const removeBook = async (bookId) => {
  if (!confirm('Вы уверены, что хотите удалить эту книгу из вашего списка?')) return
  
  try {
    removingBookId.value = bookId
    await usersApi.removeBookFromProfile(bookId)
    // Удаляем книгу из локального списка
    books.value = books.value.filter(item => item.book_id !== bookId)
  } catch (err) {
    console.error('Ошибка удаления книги:', err)
    alert(err.response?.data?.detail || 'Не удалось удалить книгу')
  } finally {
    removingBookId.value = null
  }
}

// Форматируем дату
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  loadUserBooks()
})
</script>