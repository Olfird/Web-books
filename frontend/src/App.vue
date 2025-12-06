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
              
              <li v-if="!isAuthenticated">
                <router-link to="/auth">Вход/Регистрация</router-link>
              </li>
              <li v-else>
                <router-link to="/my-books">Мои книги</router-link>
              </li>
              
              <li v-if="isAuthenticated">
                <a href="#" @click.prevent="logout" class="logout-btn">Выйти</a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </header>
    <main>
      <router-view @login="handleLogin" />
    </main>
    <footer>
      <div class="container">
        <p class="footer">&copy; BookHub. Собирай любимые произведения.</p>
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

    const handleLogin = () => {
      isAuthenticated.value = true
      router.push('/books')
    }

    const logout = () => {
      localStorage.removeItem('access_token')
      isAuthenticated.value = false
      router.push('/auth')
    }

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
  color: #ff6b6b;
  margin-left: 20px;
}

.logout-btn:hover {
  color: #ff3838;
}
</style>