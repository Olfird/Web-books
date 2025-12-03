<template>
  <main>
    <div class="container">
      <h1>Библиотека книг</h1>
      
      <div v-if="loading" class="loading">Загрузка книг...</div>
      
      <div v-else-if="error" class="error-message">
        {{ error }}
        <button @click="loadBooks" class="btn">Повторить</button>
      </div>
      
      <div v-else class="books-grid">
        <div v-for="book in books" :key="book.id" class="book-card">
          <h3>{{ book.title }}</h3>
          <p><strong>Автор:</strong> {{ book.author }}</p>
          <p><strong>Год:</strong> {{ book.year }}</p>
          <p><strong>ID:</strong> {{ book.id }}</p>
          <button 
            @click="addToMyBooks(book.id)" 
            class="btn"
            v-if="isAuthenticated"
            :disabled="addingBookId === book.id"
          >
            {{ addingBookId === book.id ? 'Добавляется...' : 'Добавить в мои книги' }}
          </button>
          <router-link v-else to="/auth" class="btn">
            Войдите, чтобы добавить
          </router-link>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../api/auth'
import { booksApi } from '../api/books'
import { usersApi } from '../api/users'

const router = useRouter()
const books = ref([])
const loading = ref(false)
const error = ref('')
const addingBookId = ref(null)

const isAuthenticated = computed(() => {
  return authApi.isAuthenticated()
})

// Загружаем список книг
const loadBooks = async () => {
  try {
    loading.value = true
    error.value = ''
    const response = await booksApi.getAllBooks()
    books.value = response.data
  } catch (err) {
    console.error('Ошибка загрузки книг:', err)
    error.value = 'Не удалось загрузить список книг'
  } finally {
    loading.value = false
  }
}

// Добавляем книгу в профиль
const addToMyBooks = async (bookId) => {
  if (!isAuthenticated.value) {
    router.push('/auth')
    return
  }
  
  try {
    addingBookId.value = bookId
    await usersApi.addBookToProfile(bookId)
    alert('Книга успешно добавлена в ваш профиль!')
  } catch (err) {
    console.error('Ошибка добавления книги:', err)
    
    const errorMsg = err.response?.data?.detail || 'Не удалось добавить книгу'
    
    if (err.response?.status === 401) {
      // Токен истек или невалидный
      alert('Ваша сессия истекла. Пожалуйста, войдите снова.')
      authApi.logout()
      router.push('/auth')
    } else if (err.response?.status === 409) {
      alert('Эта книга уже добавлена в ваш профиль!')
    } else {
      alert(errorMsg)
    }
  } finally {
    addingBookId.value = null
  }
}

onMounted(() => {
  loadBooks()
})
</script>