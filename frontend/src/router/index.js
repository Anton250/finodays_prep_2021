import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

let opts = {
  routes: [
    {
      path: "/",
      name: "Home",
      redirect: "/flat",
      // component: () => import('../components/Home.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/login",
      name: "login",
      component: () => import('../components/Login.vue'),
      meta: {
        requiresAuth: false
      }
    },
    {
      path: "/flat",
      name: "Flat",
      component: () => import('../components/Flat.vue'),
      meta: {
        requiresAuth: true
      },
    },
    {
      path: "/car",
      name: "Car",
      component: () => import('../components/Car.vue'),
      meta: {
        requiresAuth: true
      },
    },
    {
      path: "/settings",
      name: "Settings",
      component: () => import('../components/Settings.vue'),
      meta: {
        requiresAuth: true
      },
    },
  ],
  linkExactActiveClass: 'active'
};
const router = new VueRouter(opts);

export default router
