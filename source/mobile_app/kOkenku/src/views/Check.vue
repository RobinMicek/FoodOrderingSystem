<!--
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

********************************************************
-->

<template>
  <div class="h-screen overflow-y-hidden">
    
    <div class="m-5">
      <div class="mt-5">
        <button @click="getToken"
          class="bg-secondary text-white w-full p-3vh font-bold text-2xl rounded-lg focus:ring-2 focus:bg-primary ring-secondary">
          Ověřit Token
        </button>
      </div>

      <div class="mt-10">
        <p class="text-center text-lg font-bold text-white" v-if="token">{{ token.substring(0, 20) }}...</p>
      </div>
    </div>

    <div class="mt-14 text-center">
        <router-link to="/login">
          <h1 class="font-bold text-white">Přihlásit Se</h1>
        </router-link>
      </div>
  
  </div>
</template>

<script>
import { setObject, getObject } from "@/utils/storage.js"

export default {
  data() {
    return {
      token: null
    };
  },

  methods: {
    async getToken() {
      try {
        const value = await getObject("token");
        this.token = value
      } catch (error) {
        this.token = "Nepodařilo se získat token!"
      }
    },
  },
};
</script>