import Vue from 'vue';
import Router from 'vue-router';
import HomeLab from '../views/HomeLab.vue';

Vue.use(Router);

const router = new Router({
  mode: 'hash',
  routes: [
    { path: '/', name: 'home', component: HomeLab },
    { path: '/components', name: 'components', component: () => import('../views/ComponentsLab.vue') },
    { path: '/events', name: 'events', component: () => import('../views/EventsLab.vue') },
    { path: '/reactivity', name: 'reactivity', component: () => import('../views/ReactivityLab.vue') },
    { path: '/vuex', name: 'vuex', component: () => import('../views/VuexLab.vue') },
    { path: '/network', name: 'network', component: () => import('../views/NetworkLab.vue') },
    { path: '/performance', name: 'performance', component: () => import('../views/PerformanceLab.vue') },
    { path: '/lifecycle', name: 'lifecycle', component: () => import('../views/LifecycleLab.vue') },
    { path: '/debugging', name: 'debugging', component: () => import('../views/DebuggingLab.vue') },
    { path: '*', redirect: '/' }
  ],
  scrollBehavior() {
    return { x: 0, y: 0 };
  }
});

export default router;
