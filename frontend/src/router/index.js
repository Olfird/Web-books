import { createRouter, createWebHistory } from 'vue-router'
import Content from '../views/Content.vue'
import Books from '../views/Books.vue'
import Auth from '../views/Auth.vue'
import MyBooks from '../views/MyBooks.vue'

// Защищенный роут - требует авторизации
const requireAuth = (to, from, next) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    next()
  } else {
    next('/auth')
  }
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/content' },
    { path: '/content', component: Content },
    { path: '/books', component: Books },
    { path: '/auth', component: Auth },
    { 
      path: '/my-books', 
      component: MyBooks,
      beforeEnter: requireAuth
    }
  ],
})

export default router