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
    <div class="h-full">
      
      <div class="mx-5vw mt-5vh flex justify-center">
        <img src="@/assets/images/logo.png" class="w-1/3">
      </div>
  
      <div class="m-5vw">
      
        <form @submit.prevent="register">
            <InputComponent type="text" id="firstname" name="Jméno" v-model="firstname" />
            <InputComponent type="text" id="surname" name="Příjmení" v-model="surname" />
            <InputComponent type="email" id="email" name="Emailová Adresa" v-model="email" />
            <InputComponent type="tel" id="phone" name="Telefonní Číslo" v-model="phone" />
            <InputComponent type="date" id="dateOfBirth" name="Datum Narození" v-model="dateOfBirth" />
            <InputComponent type="password" id="password" name="Heslo" v-model="password" />
            
            <div class="mt-5">
                <button type="submit"
                    class="bg-secondary text-white w-full p-3vh text-2xl rounded-lg ring-secondary font-medium">
                    Vytvořit Účet
                </button>
            </div>
        </form>
  
  
        <div class="mt-14 text-center">
          <router-link to="/login">
            <a class="page-link">
              <h1 class="text-white font-medium">Přihlásit Se</h1>
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

// Import Variables
import { serverUrl } from "@/variables.js"

export default {
  data() {
    return {
      firstname: null,
      surname: null,
      email: null,
      phone: null,
      dateOfBirth: null,
      password: null
    };
  },

  // Register Components
   components: {
      InputComponent
  },

  methods: {
    async register() {
      try {
        const response = await axios.post(serverUrl + "/api/register", {
          firstname: this.firstname,
          surname: this.surname,
          email: this.email,
          phone: this.phone,
          dateOfBirth: this.dateOfBirth,
          password: this.password,
        });

        if (response && response.status === 200) {
          location.replace("/login");

        } else if (response && response.status === 400) {
            this.status = response.status
        } else {
          this.status = "error"
        }
      } catch (error) {
        console.error("Error during login:", error);
        alert("Registrace se nezdařila!")
      }
    }
  }
}
</script>
