import { createRouter, createWebHistory } from 'vue-router'
import Content from '../views/Content.vue'
import Books from '../views/Books.vue'
import Auth from '../views/Auth.vue'
import MyBooks from '../views/MyBooks.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/content' },
    { path: '/content', component: Content },
    { path: '/books', component: Books },
    { path: '/auth', component: Auth },
    { path: '/my-books', component: MyBooks, meta: { requiresAuth: true } }
  ],
})

// Добавляем навигационную защиту
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('access_token')
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/auth')
  } else {
    next()
  }
})

export default router