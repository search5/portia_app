import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: () => import('../views/IndexView.vue')
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/goods',
      name: 'goods_list',
      component: () => import('../views/GoodsView.vue')
    },
    {
      path: '/goods/:id',
      name: 'goods_view',
      component: () => import('../views/GoodsDetailView.vue')
    },
    {
      path: '/login',
      name: 'portia_login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/join_member',
      name: 'portia_join',
      component: () => import('../views/JoinView.vue')
    },
    {
      path: '/basket',
      name: 'basket_list',
      component: () => import('../views/BasketView.vue')
    },
    {
      path: '/tracking',
      name: 'tracking_view',
      component: () => import('../views/TrackingView.vue')
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: () => import('../views/MyPageView.vue')
    },
    {
      path: '/mypage/orders',
      name: 'myorder',
      component: () => import('../views/MyOrdersView.vue')
    },,
    {
      path: '/mypage/orders/:uuid',
      name: 'myorder_detail',
      component: () => import('../views/MyOrderDetail.vue')
    },
    {
      path: '/mypage/myinfo',
      name: 'myinfo',
      component: () => import('../views/MyInfoView.vue')
    }
  ]
})

export default router
