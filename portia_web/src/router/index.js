import { createRouter, createWebHistory } from 'vue-router'
import jwt_decode from "jwt-decode"

const requireAuth = () => (to, from, next) => {
  let accessToken = localStorage.getItem('access_token')
  if (accessToken !== '') {
    return next();
  }

  next('/login');
};

const requireAdminAuth = () => (to, from, next) => {
  let accessToken = localStorage.getItem('access_token')
  if (accessToken !== '' && jwt_decode(accessToken).is_admin) {
    return next();
  }

  next('/login');
};

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: () => import('../views/IndexView.vue')
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
      component: () => import('../views/BasketView.vue'),
      beforeEnter: requireAuth()
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: () => import('../views/MyPageView.vue'),
      beforeEnter: requireAuth()
    },
    {
      path: '/mypage/orders',
      name: 'myorder',
      component: () => import('../views/MyOrdersView.vue'),
      beforeEnter: requireAuth()
    },
    {
      path: '/mypage/orders/:uuid',
      name: 'myorder_detail',
      component: () => import('../views/MyOrderDetailView.vue'),
      beforeEnter: requireAuth()
    },
    {
      path: '/payment',
      name: 'payment_view',
      component: () => import('../views/PaymentView.vue'),
      beforeEnter: requireAuth()
    },
    {
      path: '/mypage/myinfo',
      name: 'myinfo',
      component: () => import('../views/MyInfoView.vue'),
      beforeEnter: requireAuth()
    },
    {
      path: '/blank-image/:size',
      name: 'blank_image',
      component: () => import('../components/icons/EmptyPicture.vue'),
      props: true
    },
    {
      path: '/admin/goods/register',
      name: 'admin_goods_register',
      component: () => import('../views/admin/GoodsRegisterView.vue'),
      beforeEnter: requireAdminAuth()
    },
    {
      path: '/admin/goods/:id',
      name: 'admin_goods_view',
      component: () => import('../views/admin/GoodsDetailView.vue'),
      beforeEnter: requireAdminAuth()
    },
    {
      path: '/admin/goods/:id/modify',
      name: 'admin_goods_modify',
      component: () => import('../views/admin/GoodsModifyView.vue'),
      beforeEnter: requireAdminAuth()
    },
    {
      path: '/admin/goods',
      name: 'admin_goods_list',
      component: () => import('../views/admin/GoodsListView.vue'),
      beforeEnter: requireAdminAuth()
    }
  ]
})

export default router
