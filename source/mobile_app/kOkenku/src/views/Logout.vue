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

    <div class="flex flex-col items-center mx-5vw my-5vh"> 
        <Loading />
    </div>

</template>


<script>
// Import Components
import Loading from "@/components/Loading.vue"

// Import Modules 

// Import JS
import { removeObject } from "@/utils/storage.js"

// Import Variables
export default {
  data() {
    return {
        
    }
  },
  
  // Register Components
  components: {
    Loading
  },

  mounted() {
    this.logout()
  },
  
  methods: {
    async logout() {
        await removeObject("token")
        await removeObject("cardNumber")
        location.replace("/login")
    }
  }

}
</script>