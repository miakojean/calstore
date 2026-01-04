import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path:'/discounts',
      name:'discounts',
      component: () => import('../views/DiscountView.vue'),
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    // === Routes for managing products and cart ===
    {
      path: '/cart-checkout',
      name: 'cart-checkout',
      component: () => import('../views/CartCheckoutView.vue'),
    }
  ],
})

export default router
