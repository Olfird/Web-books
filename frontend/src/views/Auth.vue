<template>
  <main>
    <div class="container">
      <div class="auth-container">
        <div class="card">
          <div class="auth-tabs">
            <button 
              type="button"
              :class="['auth-tab', { active: activeTab === 'login' }]" 
              @click="switchTab('login')"
            >
              Вход
            </button>
            <button 
              type="button"
              :class="['auth-tab', { active: activeTab === 'register' }]" 
              @click="switchTab('register')"
            >
              Регистрация
            </button>
          </div>
          
          <!-- Форма входа -->
          <div v-if="activeTab === 'login'">
            <form @submit.prevent="handleLogin">
              <div class="form-group">
                <label>Имя пользователя</label>
                <input 
                  type="text" 
                  v-model="loginForm.username" 
                  required
                  :disabled="loading"
                >
              </div>
              <div class="form-group">
                <label>Пароль</label>
                <input 
                  type="password" 
                  v-model="loginForm.password" 
                  required
                  :disabled="loading"
                >
              </div>
              <button type="submit" class="btn" :disabled="loading">
                {{ loading ? 'Вход...' : 'Войти' }}
              </button>
            </form>
            
            <div v-if="loginError" class="error-message">{{ loginError }}</div>
            <div v-if="loginDebug" class="debug-info">
              <small>{{ loginDebug }}</small>
            </div>
          </div>
          
          <!-- Форма регистрации -->
          <div v-else>
            <form @submit.prevent="handleRegister">
              <div class="form-group">
                <label>Имя пользователя</label>
                <input 
                  type="text" 
                  v-model="registerForm.username" 
                  required
                  :disabled="loading"
                >
                <small class="hint">Минимум 3 символа</small>
              </div>
              <div class="form-group">
                <label>Пароль</label>
                <input 
                  type="password" 
                  v-model="registerForm.password" 
                  required
                  :disabled="loading"
                >
                <small class="hint">Минимум 6 символов</small>
              </div>
              <button type="submit" class="btn" :disabled="loading">
                {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
              </button>
            </form>
            
            <div v-if="registerError" class="error-message">{{ registerError }}</div>
            <div v-if="registerDebug" class="debug-info">
              <small>{{ registerDebug }}</small>
            </div>
            <div v-if="registerSuccess" class="success-message">
              ✅ Регистрация успешна! Теперь вы можете войти.
            </div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../api/auth'
import { usersApi } from '../api/users'

const router = useRouter()

const activeTab = ref('login')
const loading = ref(false)
const loginError = ref('')
const loginDebug = ref('')
const registerError = ref('')
const registerDebug = ref('')
const registerSuccess = ref(false)

const loginForm = ref({
  username: '',
  password: ''
})

const registerForm = ref({
  username: '',
  password: ''
})

const switchTab = (tab) => {
  activeTab.value = tab
  loginError.value = ''
  loginDebug.value = ''
  registerError.value = ''
  registerDebug.value = ''
  registerSuccess.value = false
}

const handleLogin = async (event) => {
  console.log('🔵 handleLogin вызван')
  
  // Важно: предотвращаем поведение по умолчанию
  if (event) {
    event.preventDefault()
    event.stopPropagation()
  }
  
  // Сброс ошибок
  loginError.value = ''
  loginDebug.value = ''
  
  // Базовая валидация
  if (!loginForm.value.username.trim()) {
    loginError.value = 'Введите имя пользователя'
    return
  }
  
  if (!loginForm.value.password.trim()) {
    loginError.value = 'Введите пароль'
    return
  }
  
  if (loginForm.value.password.length < 6) {
    loginError.value = 'Пароль должен быть не менее 6 символов'
    return
  }

  try {
    loading.value = true
    loginDebug.value = 'Отправка запроса...'
    
    console.log('📤 Данные для входа:', {
      username: loginForm.value.username,
      password: '***'
    })
    
    // Отправляем запрос
    const response = await authApi.login(
      loginForm.value.username, 
      loginForm.value.password
    )
    
    console.log('✅ Ответ сервера:', response)
    
    if (response.data?.access_token) {
      // Сохраняем токен
      localStorage.setItem('access_token', response.data.access_token)
      console.log('🔑 Токен сохранен в localStorage')
      
      // Проверяем сохранение
      const savedToken = localStorage.getItem('access_token')
      if (savedToken) {
        loginDebug.value = 'Успешно! Перенаправляем...'
        
        // Маленькая задержка для визуальной обратной связи
        setTimeout(() => {
          router.push('/my-books')
        }, 500)
      } else {
        loginError.value = 'Ошибка сохранения токена'
      }
    } else {
      loginError.value = 'Сервер не вернул токен'
    }
    
  } catch (err) {
    console.error('❌ Ошибка входа:', err)
    
    if (err.response?.status === 401) {
      loginError.value = 'Неверное имя пользователя или пароль'
    } else if (err.response?.data?.detail) {
      loginError.value = err.response.data.detail
    } else if (err.message.includes('Network Error')) {
      loginError.value = 'Нет соединения с сервером. Убедитесь, что бэкенд запущен.'
    } else {
      loginError.value = err.message || 'Ошибка входа'
    }
    
    loginDebug.value = `Ошибка: ${err.message}`
    
  } finally {
    loading.value = false
  }
}

const handleRegister = async (event) => {
  console.log('🔵 handleRegister вызван')
  
  // Предотвращаем поведение по умолчанию
  if (event) {
    event.preventDefault()
    event.stopPropagation()
  }
  
  registerError.value = ''
  registerDebug.value = ''
  
  // Валидация
  if (!registerForm.value.username.trim()) {
    registerError.value = 'Введите имя пользователя'
    return
  }
  
  if (!registerForm.value.password.trim()) {
    registerError.value = 'Введите пароль'
    return
  }
  
  if (registerForm.value.username.length < 3) {
    registerError.value = 'Имя пользователя должно быть не менее 3 символов'
    return
  }
  
  if (registerForm.value.password.length < 6) {
    registerError.value = 'Пароль должен быть не менее 6 символов'
    return
  }

  try {
    loading.value = true
    registerDebug.value = 'Отправка запроса...'
    
    console.log('📤 Данные для регистрации:', {
      username: registerForm.value.username,
      password: '***'
    })
    
    await usersApi.register(registerForm.value)
    
    console.log('✅ Регистрация успешна')
    
    // Успешная регистрация
    registerSuccess.value = true
    registerDebug.value = 'Успешно!'
    
    // Очищаем форму
    registerForm.value = { username: '', password: '' }
    
    // Через 1.5 секунды переключаем на вкладку входа
    setTimeout(() => {
      activeTab.value = 'login'
      registerSuccess.value = false
      registerDebug.value = ''
    }, 1500)
    
  } catch (err) {
    console.error('❌ Ошибка регистрации:', err)
    
    if (err.response?.status === 409) {
      registerError.value = 'Пользователь с таким именем уже существует'
    } else if (err.response?.data?.detail) {
      registerError.value = err.response.data.detail
    } else if (err.message.includes('Network Error')) {
      registerError.value = 'Нет соединения с сервером'
    } else {
      registerError.value = err.message || 'Ошибка регистрации'
    }
    
    registerDebug.value = `Ошибка: ${err.message}`
    
  } finally {
    loading.value = false
  }
}

// Добавляем обработчик для клавиши Enter
const handleKeyPress = (event) => {
  if (event.key === 'Enter') {
    if (activeTab.value === 'login') {
      handleLogin(event)
    } else {
      handleRegister(event)
    }
  }
}

// Добавляем обработчик событий при монтировании
import { onMounted, onUnmounted } from 'vue'

onMounted(() => {
  document.addEventListener('keypress', handleKeyPress)
})

onUnmounted(() => {
  document.removeEventListener('keypress', handleKeyPress)
})
</script>

<style scoped>
.auth-tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 2px solid #eee;
}

.auth-tab {
  flex: 1;
  padding: 10px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #666;
  transition: all 0.3s;
  position: relative;
}

.auth-tab:hover {
  background-color: #f5f5f5;
}

.auth-tab.active {
  color: #3498db;
  font-weight: bold;
}

.auth-tab.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #3498db;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box;
}

.form-group input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.form-group input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.hint {
  display: block;
  color: #7f8c8d;
  font-size: 12px;
  margin-top: 5px;
}

.btn {
  width: 100%;
  padding: 12px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: #2980b9;
}

.btn:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.error-message {
  margin-top: 15px;
  padding: 10px;
  background-color: #ffeaea;
  color: #e74c3c;
  border-radius: 4px;
  border: 1px solid #e74c3c;
}

.success-message {
  margin-top: 15px;
  padding: 10px;
  background-color: #eaffea;
  color: #27ae60;
  border-radius: 4px;
  border: 1px solid #27ae60;
}

.debug-info {
  margin-top: 10px;
  padding: 8px;
  background-color: #f5f5f5;
  color: #666;
  border-radius: 4px;
  font-size: 12px;
}
</style>