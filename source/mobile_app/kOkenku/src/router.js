/*
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

********************************************************
*/


import { createRouter, createWebHistory } from 'vue-router'
import { getObject } from "@/utils/storage.js"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      component: () => import('@/views/Login.vue'),
    },
    {
      path: '/register',
      component: () => import('@/views/Register.vue'),
    },

    {
      path: '/',
      component: () => import('@/views/Home.vue'),
    },
    {
      path: '/navbar',
      component: () => import('@/views/NavBar.vue'),
    },
    
    
    {
      path: '/wallet',
      component: () => import('@/views/Wallet.vue'),
    },


    {
      path: '/orders',
      component: () => import('@/views/Orders.vue'),
    },
    {
      path: '/order',
      name: 'order',
      component: () => import('@/views/Order.vue'),
    },


    {
      path: '/establishments',
      component: () => import('@/views/Establishments.vue'),
    },
    {
      path: '/menus',
      name: 'menus',
      component: () => import('@/views/Menus.vue'),
    },
    {
      path: '/products',
      name: 'products',
      component: () => import('@/views/Products.vue'),
    },
    {
      path: '/checkout',
      name: 'checkout',
      component: () => import('@/views/Checkout.vue'),
    },


    {
      path: '/establishments-list',
      component: () => import('@/views/EstablishmentList.vue'),
    },
    {
      path: '/terms',
      component: () => import('@/views/Terms.vue'),
    },
    {
      path: '/contact',
      component: () => import('@/views/Contact.vue'),
    },


    {
      path: '/logout',
      component: () => import('@/views/Logout.vue'),
    }
  ],
});



// Add a login guard
router.beforeEach(async (to, from, next) => {
  try {
    const token = await getObject("token"); // Wait for the promise to resolve
    if (to.path !== '/login' && to.path !== '/register' && !token) {
      next('/login'); // Redirect to login if token does not exist
    } else {
      next(); // Continue to the requested route
    }
  } catch (error) {
    console.error("Error retrieving token:", error);
    next('/login')
  }
});

export default router;