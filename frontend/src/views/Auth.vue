<template>
  <main>
    <div class="container">
      <div class="auth-container">
        <div class="card">
          <div class="auth-tabs">
            <button :class="['auth-tab', { 'active': activeTab === 'login' }]" @click="activeTab = 'login'">
              Вход
            </button>
            <button :class="['auth-tab', { 'active': activeTab === 'register' }]" @click="activeTab = 'register'">
              Регистрация
            </button>
          </div>
          
          <!-- Форма входа -->
          <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="auth-form">
            <div class="form-group">
              <label for="login-username">Имя пользователя</label>
              <input type="text" v-model="loginData.username" />
            </div>
            <div class="form-group">
              <label for="login-password">Пароль</label>
              <input type="password" v-model="loginData.password" />
            </div>
            
            <button type="submit" class="btn" :disabled="loginLoading">
              {{ loginLoading ? 'Вход...' : 'Войти' }}
            </button>
          </form>
          
          <!-- Форма регистрации -->
          <form v-if="activeTab === 'register'" @submit.prevent="handleRegister" class="auth-form">
            <div class="form-group">
              <label for="register-username">Имя пользователя</label>
              <input type="text" v-model="registerData.username" />
            </div>
            <div class="form-group">
              <label for="register-password">Пароль</label>
              <input type="password" v-model="registerData.password" />
            </div>
            <div class="form-group">
              <label for="confirm-password">Подтвердите пароль</label>
              <input type="password" v-model="registerData.confirmPassword" />
            </div>
            
            <div v-if="registerError" class="error-message">
              {{ registerError }}
            </div>
            
            <div v-if="registerSuccess" class="success-message">
              Регистрация успешна! Теперь вы можете войти.
            </div>
            
            <button type="submit" class="btn" :disabled="registerLoading">
              {{ registerLoading ? 'Регистрация...' : 'Зарегистрироваться' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '../api/auth'

export default {
  name: 'AuthPage',
  emits: ['login'],
  setup(props, { emit }) {
    const router = useRouter()
    
    const activeTab = ref('login')
    
    const loginData = ref({
      username: '',
      password: ''
    })
    
    const registerData = ref({
      username: '',
      password: '',
      confirmPassword: ''
    })
    
    const loginLoading = ref(false)
    const registerLoading = ref(false)
    const loginError = ref('')
    const registerError = ref('')
    const registerSuccess = ref(false)

    const handleLogin = async () => {
      loginLoading.value = true
      loginError.value = ''
      
      try {
        const response = await authAPI.login(
          loginData.value.username, 
          loginData.value.password
        )
        
        localStorage.setItem('access_token', response.data.access_token)
        
        emit('login')
        
        router.push('/books')
        
      } catch (error) {
        loginError.value = error.response?.data?.detail?.[0]?.msg || 
                          error.response?.data?.detail || 
                          'Ошибка входа. Проверьте данные.'
      } finally {
        loginLoading.value = false
      }
    }

    const handleRegister = async () => {
      if (registerData.value.password !== registerData.value.confirmPassword) {
        registerError.value = 'Пароли не совпадают'
        return
      }
      
      registerLoading.value = true
      registerError.value = ''
      registerSuccess.value = false
      
      try {
        await authAPI.register(
          registerData.value.username, 
          registerData.value.password
        )
        
        registerSuccess.value = true
        
        // Очищаем форму
        registerData.value = {
          username: '',
          password: '',
          confirmPassword: ''
        }
        
        setTimeout(() => {
          activeTab.value = 'login'
          registerSuccess.value = false
        }, 2000)
        
      } catch (error) {
        console.error('Registration error:', error)
        registerError.value = error.response?.data?.detail?.[0]?.msg || 
                             error.response?.data?.detail || 
                             'Ошибка регистрации. Попробуйте другой логин.'
      } finally {
        registerLoading.value = false
      }
    }

    return {
      activeTab,
      loginData,
      registerData,
      loginLoading,
      registerLoading,
      loginError,
      registerError,
      registerSuccess,
      handleLogin,
      handleRegister
    }
  }
}
</script>

<style scoped>
.auth-form {
  display: block;
}
</style>