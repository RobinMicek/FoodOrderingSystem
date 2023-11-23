import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import VueFeather from 'vue-feather';

import('@/assets/main.css');

createApp(App)
    .component(VueFeather.name, VueFeather)
    .use(router)
    .mount('#app')
