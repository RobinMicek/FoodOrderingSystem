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
    
    <TopBar backLink="/" text="Provozovny"/>

    <div class="h-full flex flex-col items-center mx-5vw my-5vh">

        <div v-if="establishments && establishments.length != 0" class="w-full">
            <pull-to-refresh @refresh="refreshData">
                <div v-for="establishment in establishments">                    
                    
                    <div class="mb-3vh relative grid grid-cols-3 w-full bg-white rounded-lg">
                        
                        <div class="col-span-1">
                            <img :src="serverUrl + establishment.imagePath" class="h-full w-full object-cover rounded-tl-lg rounded-bl-lg">
                        </div>

                        <div class="col-span-2 p-2vh">                      
                            <h1 class="text-secondary font-medium">{{ establishment.name }}</h1>   
                            <h1 class="text-xs pb-2">{{ establishment.address }}</h1>                               
                            
                            <div class="mb-5 overflow-x-scroll whitespace-nowrap flex gap-3">
                                <img v-if="establishment.wifi" src="@/assets/icons/wifi.png" alt="Wifi" class="h-5">
                                <img v-if="establishment.parking" src="@/assets/icons/parking.png" alt="Parking" class="h-5">
                                <img v-if="establishment.dineIn" src="@/assets/icons/dineIn.png" alt="Dine In" class="h-5">
                                <img v-if="establishment.yard" src="@/assets/icons/yard.png" alt="Yard" class="h-5">
                                <img v-if="establishment.playground" src="@/assets/icons/playground.png" alt="Playground" class="h-5">
                                <img v-if="establishment.eCharger" src="@/assets/icons/eCharger.png" alt="E Charger" class="h-5">
                            </div>

                            <div class="absolute bottom-0 pb-2">
                                <h1 class="text-sm font-medium">
                                    <span v-if="establishment.isOpen.isOpen" class="text-green-600">
                                        {{ establishment.isOpen.openingTime }} - {{ establishment.isOpen.closingTime }}
                                    </span>
                                    <span v-else class="text-red-500">
                                        {{ establishment.isOpen.openingTime }} - {{ establishment.isOpen.closingTime }}
                                    </span>
                                </h1>          
                            </div>
                        </div>

                    </div>
                
                </div>
            </pull-to-refresh>
        </div>

        <div v-else-if="establishments && establishments.length === 0">
            <h1 class="text-lg text-center text-white">Nejsou dostupné žádné provozovny!</h1>
        </div>

        <div v-else>
            <Loading />
        </div>
    </div>

</template>


<script>
// Import Components
import TopBar from "@/components/TopBar.vue"
import Loading from "@/components/Loading.vue"
import PullToRefresh from "@/components/PullToRefresh.vue"

// Import Modules 
import axios from 'axios'
import { Haptics } from "@capacitor/haptics"

// Import JS
import { getObject, removeObject } from "@/utils/storage.js"

// Import Variables
import { serverUrl } from "@/variables.js"

export default {
  data() {
    return {
        serverUrl,
        establishments: null,
    }
  },
  
  // Register Components
  components: {
    TopBar,
    Loading,
    PullToRefresh
  },

  mounted() {
    this.getAllEstablishments()
  },
  
  methods: {
    async getAllEstablishments() {
        try {
            const token = await getObject("token")
            
            const response = await axios.get(serverUrl + "/api/get-all-establishments", {
                headers: {
                "Authorization": token 
                }
            });

            if (response && response.status === 200) {
                this.establishments = response.data.data
            }
            
        } catch (error) {
            await removeObject("token")
            location.replace("/login")
        }
    },

    async refreshData() {
        await Haptics.impact()

        this.establishments = null
        await this.getAllEstablishments()   
    }
  }

}
</script>