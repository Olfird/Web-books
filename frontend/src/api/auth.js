import apiClient from './index'

export const authApi = {
  // Вход в систему
  async login(username, password) {
    console.log('🔵 [authApi.login] Начало')
    
    // Создаем FormData правильным образом
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    
    console.log('📦 FormData:', formData.toString())
    
    try {
      console.log('🔄 Отправка POST на /auth/login')
      
      const response = await apiClient.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
      
      console.log('✅ Успешный ответ:', response.status)
      console.log('📊 Данные ответа:', response.data)
      
      return response
      
    } catch (error) {
      console.error('❌ Ошибка запроса:', error)
      
      // Подробная информация об ошибке
      if (error.response) {
        console.error('📡 Статус ошибки:', error.response.status)
        console.error('📡 Данные ошибки:', error.response.data)
        console.error('📡 Заголовки ошибки:', error.response.headers)
      } else if (error.request) {
        console.error('📡 Нет ответа от сервера:', error.request)
      } else {
        console.error('📡 Ошибка настройки запроса:', error.message)
      }
      
      console.error('📡 Конфиг запроса:', error.config)
      
      throw error
    }
  },

  // Проверка авторизации
  isAuthenticated() {
    const token = localStorage.getItem('access_token')
    return !!token
  },

  // Выход из системы
  logout() {
    localStorage.removeItem('access_token')
  },

  // Получение пользователя из токена
  getUserFromToken() {
    const token = localStorage.getItem('access_token')
    if (!token) return null
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      return {
        username: payload.sub
      }
    } catch (error) {
      console.error('Ошибка парсинга токена:', error)
      return null
    }
  }
}