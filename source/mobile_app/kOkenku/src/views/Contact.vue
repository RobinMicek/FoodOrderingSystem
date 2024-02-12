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
    
    <TopBar backLink="/" text="Kontakt"/>

    <div class="mx-5vw my-5vh">

        <div v-if="configuration && configuration.length != 0">
            <div class="text-white">
                <h1 class="text-white text-2xl">{{ configuration.companyInfo.companyName }}</h1>
            </div>

            <div class="mt-10">
                <div class="mb-10">
                    <div class="text-white flex gap-x-3 items-center justify-left w-full h-full">                
                        <vue-feather type="map" size="24" class="text-secondary"/>
                        Adresa Společnosti
                    </div>
                    <div class="mt-2">
                        <p class="text-white">{{ configuration.companyInfo.address  }}</p>
                    </div>
                </div>
                
                <div class="mb-10">
                    <div class="text-white flex gap-x-3 items-center justify-left w-full h-full">                
                        <vue-feather type="phone" size="24" class="text-secondary"/>
                        Telefonní Číslo
                    </div>
                    <div class="mt-2">
                        <p class="text-white">{{ configuration.companyInfo.phone  }}</p>
                    </div>
                </div>
                
                <div class="mb-10">
                    <div class="text-white flex gap-x-3 items-center justify-left w-full h-full">                
                        <vue-feather type="mail" size="24" class="text-secondary"/>
                        Emailová Adresa
                    </div>
                    <div class="mt-2">
                        <p class="text-white">{{ configuration.companyInfo.email  }}</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div v-else class="flex flex-col h-full w-full items-center">
            <Loading />
        </div>
    </div>

</template>


<script>
// Import Components
import TopBar from "@/components/TopBar.vue"
import Loading from "@/components/Loading.vue"

// Import Modules

// Import JS

// Import Variables
import { getConfiguration } from "@/variables.js"

export default {
  data() {
    return {
        configuration: null,
    }
  },
  
  // Register Components
  components: {
    TopBar,
    Loading
  },

  mounted() {
    this.getConfig()
  },
  
  methods: {
    async getConfig() {
        this.configuration = await getConfiguration()
    }
  }

}
</script>