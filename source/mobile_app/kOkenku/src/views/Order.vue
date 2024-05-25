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
    <TopBar backLink="/orders" text="Objednávka"/>        

        <div v-if="order && configuration" class="mt-10">       
            <pull-to-refresh @refresh="refreshData">
            
                <div class="m-5vw text-white">
                    <div>
                        <div v-if="order.tag" class="border-b-2 text-white p-5">
                            <div>
                                <h1 class="text-4xl text-center font-medium">{{ String(order.tag).padStart(3, '0') }}</h1>
                                <h1 class="text-sm text-center">Vyvolávací Kód</h1>
                            </div>

                            <div v-if="configuration.app.generateQRCodes" class="flex w-full items-center justify-center">
                                <vue-qrcode class=""
                                    :value="qrCodeText" 
                                    :options="{ 
                                        width: 200,
                                        color: {
                                            dark: '#008550',
                                            light: '212121'
                                        }
                                    }"></vue-qrcode>
                            </div>

                            <div v-else class="mb-5"></div> <!-- Spacing between items (Disabled when QR code is shown)-->

                            <div class="text-2xl text-white">                    
                                <div>
                                    <h1 class="text-center font-medium uppercase">
                                        <p v-if="order.status == 'CANCELED'" class="text-red-500">Zrušená</p>    
                                        <p v-else-if="order.status == 'CREATED'" class="text-green-600">Přijatá</p>    
                                        <p v-else-if="order.status == 'PROCESSING'" class="text-green-600">Připravuje Se</p>    
                                        <p v-else-if="order.status == 'READY'" class="text-green-600">K Vyzvedutí</p>    
                                        <p v-else-if="order.status == 'DONE'" class="text-green-600">Vydaná</p>    
                                        <p v-else>Neznámý Stav</p>    
                                    </h1>
                                </div>
                            </div>
                        </div>

                        <h1 class="mt-5 text-center font-medium">{{ order.name }}</h1>
                    </div>
                    
                    <div class="mt-10 grid grid-cols-3">
                        <div class="col-span-1 text-left">
                            <p class="text-sm mb-2">Typ Platby:</p>
                            <p class="text-sm">Čas Objednání:</p>
                            <p class="text-sm">Čas Vyzvednutí:</p>
                        </div>
                        <div class="col-span-2 text-right">
                            <p class="text-sm font-medium mb-2">{{ order.paymentType == "WALLET" ? "PENĚŽENKA" : "HOTOVOST  " }}</p>
                            <p class="text-sm font-medium">{{ (new Date(new Date(order.createdTime) - new Date(order.createdTime).getTimezoneOffset() * (-60000))).toLocaleString(configuration.app.dateTime.timezone, configuration.app.dateTime) }}</p>
                            <p class="text-sm font-medium">{{ (new Date(new Date(order.pickupTime) - new Date(order.createdTime).getTimezoneOffset() * (-60000))).toLocaleString(configuration.app.dateTime.timezone, configuration.app.dateTime) }}</p>
                        </div>
                    </div>
                </div>

                <div class="mt-20 m-5vw text-white">

                    <div class="w-full text-left text-sm">
                        <table class="min-w-full table-auto">
                            <thead>
                                <tr>
                                    <th class="px-1 py-1">Produkt</th>
                                    <th class="px-1 py-1 text-right">Cena</th>
                                </tr>
                            </thead>
                            <tbody v-for="product in order.products">                            
                                <tr>
                                    <td class="px-1 py-1">{{ product.quantity}}x {{ product.name}}</td>
                                    <td class="px-1 py-1 text-right">{{ (product.price * product.quantity).toFixed(2) }}</td>
                                </tr>                  
                            </tbody>
                            <tfoot>
                                <tr class="border-t-2 border-white">                                
                                    <td class="px-1 py-2 font-medium">Celkem</td>
                                    <td class="px-1 py-2 font-medium text-right whitespace-nowrap">{{order.totalPrice }} Kč</td>
                                </tr>     
                            </tfoot>
                        </table>
                    </div>
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
        order: null,
        configuration: null,
        qrCodeText: null
    }
  },
  
  // Register Components
  components: {
    TopBar,
    Loading,
    PullToRefresh
  },

  mounted() {
    this.getConfig(),
    this.getOrder()
  },
  
  methods: {
    async getConfig() {
        this.configuration = await getConfiguration()
    },

    async getOrder() {
        try {
            const orderId = new URLSearchParams(window.location.search).get("orderId")
            const token = await getObject("token")

            const response = await axios.get(serverUrl + "/api/get-order?orderId=" + orderId, {
                headers: {
                "Authorization": token 
                }
            });

            if (response && response.status === 200) {
                this.order = response.data.data
                this.qrCodeText = JSON.stringify({
                    id: this.order.orderId,
                    tag: this.order.tag
                })
            }
            
        } catch (error) {
            await removeObject("token")
            location.replace("/login")
        }
    },

    async refreshData() {
        await Haptics.impact()

        this.order = null
        await this.getOrder()
    },
  }

}
</script>