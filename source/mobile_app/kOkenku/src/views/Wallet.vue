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
    <TopBar backLink="/" text="Peněženka"/>        

        <div v-if="card && walletBalance" class="mt-5">       
            <pull-to-refresh @refresh="refreshData">

                
                <div class="w-screen flex items-center justify-center rounded-lg">
                    <vue-qrcode class=""
                    :value="card" 
                    :options="{
                        width: 300,
                            color: {
                                dark: '#FFFFFF',
                                light: '#212121'
                            }
                        }"></vue-qrcode>
                </div>
                
                
                
                
                <div class="text-center">
                    <h1 class="text-white font-semibold text-4xl">{{ walletBalance }} Kč</h1>
                    <h1 class="text-white">Aktuální Zůstatek</h1>
                </div>
                
                <div class="text-center bg-secondary text-white rounded-lg p-4 m-10">
                    <h1 class="font-semibold text-lg">{{ card }}</h1>
                    <h1 class="text-sm">Číslo Karty</h1>
                </div>
            </pull-to-refresh>                      
        </div>

        <div v-else class="flex flex-col items-center mx-5vw my-5vh"> 
            <Loading />
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
import { getConfiguration, serverUrl } from "@/variables.js"

export default {
  data() {
    return {
        card: null,
        walletBalance: null
    }
  },
  
  // Register Components
  components: {
    TopBar,
    Loading,
    PullToRefresh
  },

  mounted() {
    this.getWalletInfo()
  },
  
  methods: {
    async getWalletInfo() {
        try {
            const cardNumber = await getObject("cardNumber")
            const token = await getObject("token")

            const response = await axios.get(serverUrl + "/api/get-wallet", {
                headers: {
                "Authorization": token 
                }
            });

            if (response && response.status === 200) {
                this.walletBalance = response.data.data.walletBalance
                this.card = cardNumber
            }
            
        } catch (error) {
            await removeObject("token")
            location.replace("/login")
        }
    },

    async refreshData() {
        await Haptics.impact()

        this.card = null
        this.walletBalance = null
        await this.getWalletInfo()
    },
  }

}
</script>