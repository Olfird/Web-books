<template>
  <div id="app">
    <header>
      <div class="container">
        <div class="header-content">
          <div class="logo">BookHub</div>
          <nav>
            <ul class="nav-links">
              <li><router-link to="/content">Главная</router-link></li>
              <li><router-link to="/books">Библиотека</router-link></li>
              
              <!-- Динамическая ссылка -->
              <li v-if="!isAuthenticated">
                <router-link to="/auth">Вход/Регистрация</router-link>
              </li>
              <li v-else>
                <router-link to="/my-books">Мои книги</router-link>
              </li>
              
              <!-- Кнопка выхода -->
              <li v-if="isAuthenticated">
                <a href="#" @click.prevent="logout" class="logout-btn">Выйти</a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </header>

    <router-view @login="handleLogin" />

    <footer>
      <div class="container">
        <p>&copy; 2024 BookHub. Все права защищены.</p>
      </div>
    </footer>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const isAuthenticated = ref(false)

    // Функция проверки авторизации
    const checkAuth = () => {
      const token = localStorage.getItem('access_token')
      isAuthenticated.value = !!token
    }

    // Логин
    const handleLogin = () => {
      isAuthenticated.value = true
      router.push('/books')
    }

    // Логаут
    const logout = () => {
      localStorage.removeItem('access_token')
      isAuthenticated.value = false
      router.push('/auth')
    }

    // Следим за изменениями маршрута
    watch(() => router.currentRoute.value, () => {
      checkAuth()
    })

    onMounted(() => {
      checkAuth()
    })

    return {
      isAuthenticated,
      handleLogin,
      logout
    }
  }
}
</script>

<style scoped>
.logout-btn {
  color: #ff6b6b !important;
  margin-left: 20px !important;
}

.logout-btn:hover {
  color: #ff3838 !important;
}
</style>