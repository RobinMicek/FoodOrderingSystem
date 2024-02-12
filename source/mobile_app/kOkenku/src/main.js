/*
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

********************************************************
*/


import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import VueFeather from 'vue-feather'
import VueQrcode from '@chenfengyuan/vue-qrcode'


import('@/assets/main.css');

createApp(App)
    .component(VueFeather.name, VueFeather)
    .component(VueQrcode.name, VueQrcode)
    .use(router)
    .mount('#app')
