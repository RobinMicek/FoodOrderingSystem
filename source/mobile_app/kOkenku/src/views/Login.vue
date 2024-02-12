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
  <div class="h-screen overflow-hidden flex flex-col">
    
    <div class="mx-5vw mt-10vh flex justify-center">
      <img src="@/assets/images/logo.png" class="w-1/3">
    </div>

    <div class="m-5vw">
    
      <form @submit.prevent="login">
        <InputComponent type="email" id="email" name="Emailová Adresa" v-model="email" />
        <InputComponent type="password" id="password" name="Heslo" v-model="password" />
        
        <div class="mt-5">
          <button type="submit"
            class="bg-secondary text-white w-full p-3vh text-2xl rounded-lg ring-secondary font-medium">
            Přihlásit Se
          </button>
        </div>
      </form>


      <div class="mt-14 text-center">
        <router-link to="/register">
          <a class="page-link">
            <h1 class="text-white font-medium">Vytvořit Účet</h1>
          </a>
        </router-link>
      </div>

    </div>
  </div>
</template>


<script>
// Import Components
import InputComponent  from "@/components/InputComponent.vue"

// Import Modules 
import axios from 'axios'

// Import JS
import { setObject, getObject } from "@/utils/storage.js"

// Import Variables
import { serverUrl } from "@/variables.js"

export default {
  data() {
    return {
      email: "",
      password: ""
    };
  },
  
  // Register Components
  components: {
    InputComponent
  },

  methods: {
    async login() {
      try {
        const response = await axios.post(serverUrl + "/api/login", {
          email: this.email,
          password: this.password,
        });

        if (response && response.status === 200) {
          await setObject("token", response.data.token);
          location.replace("/");
        } else {
          this.msg = "Přihlášení se nezdařilo!";
        }
      } catch (error) {
        console.error("Error during login:", error);
        alert("Přihlášení se nezdařilo!")
      }
    }
  }
}
</script>





