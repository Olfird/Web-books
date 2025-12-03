<template>
  <header>
    <div class="header-content">
      <div class="logo">BookHub</div>
      <div class="nav-links">
        <router-link to="/content">Главная</router-link>
        <router-link to="/books">Библиотека</router-link>
        <router-link v-if="isAuthenticated" to="/my-books">Мои книги</router-link>
        <router-link v-else to="/auth">Вход</router-link>
        <button v-if="isAuthenticated" @click="logout" class="logout-btn">Выйти</button>
        <span v-if="isAuthenticated" class="username">Привет, {{ username }}!</span>
      </div>
    </div>
  </header>

  <main>
    <router-view />
  </main>

  <footer>
    <div class="container">
      <p>Каталог прочитанных книг © 2024</p>
    </div>
  </footer>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from './api/auth'

const router = useRouter()
const username = ref('')

const isAuthenticated = computed(() => {
  return authApi.isAuthenticated()
})

// При загрузке получаем имя пользователя
onMounted(() => {
  const user = authApi.getUserFromToken()
  if (user) {
    username.value = user.username
  }
})

// Выход из системы
const logout = () => {
  authApi.logout()
  username.value = ''
  router.push('/auth')
}
</script>