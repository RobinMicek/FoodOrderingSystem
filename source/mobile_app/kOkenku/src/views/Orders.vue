<template>
    
    <TopBar backLink="/" text="Moje Objednávky"/>

    <div class="h-full flex flex-col items-center mx-5vw my-5vh">
        
        <div v-if="orders && orders.length != 0 && configuration" class="w-full">
            <pull-to-refresh @refresh="refreshData">

                <div v-for="order in orders">                    
                
                    <router-link :to="{ name: 'order', query: { orderId: order.orderId } }">
                        <div class="mb-3vh relative grid grid-cols-2 w-full p-2vh bg-white rounded-lg">
                            
                            <div class="col-span-1">
                                <div v-if="order.tag">
                                    <h1 class="text-lg font-medium">{{ String(order.tag).padStart(3, '0') }}</h1>
                                </div>
                                
                                <p class="mt-1 text-sm">{{ order.name }}</p>
                                <p class="mt-1 text-sm font-medium">{{ (new Date(new Date(order.createdTime) - new Date(order.createdTime).getTimezoneOffset() * (-60000))).toLocaleString(configuration.app.dateTime.timezone, configuration.app.dateTime) }}</p>                            
                                
                                
                            </div>

                            <div class="col-span-1 h-full flex flex-col justify-center text-right">                                
                                <div v-if="order.tag">
                                    <h1 class="mt-2 text-md text-secondary font-medium uppercase">
                                        <p v-if="order.status == 'CANCELED'" class="text-red-500">Zrušená</p>    
                                        <p v-else-if="order.status == 'CREATED'" class="text-green-600">Přijatá</p>    
                                        <p v-else-if="order.status == 'PROCESSING'" class="text-green-600">Připravuje Se</p>    
                                        <p v-else-if="order.status == 'READY'" class="text-green-600">K Vyzvedutí</p>    
                                        <p v-else-if="order.status == 'DONE'" class="text-green-600">Vydaná</p>    
                                        <p v-else>Neznámý Stav</p>                                            
                                    </h1>
                                </div>

                                <div class="">                            
                                    <p class="mt-1 text-lg font-medium">{{ order.totalPrice }} Kč</p>
                                </div>   
                            </div>

                        </div>
                    </router-link>
                
                </div>
            </pull-to-refresh>
        </div>
        

        <div v-else-if="orders && orders.length === 0">
            <h1 class="text-lg text-center text-white">Nemáte ještě žádné objednávky!</h1>
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
import { getConfiguration, serverUrl } from "@/variables.js"

export default {
  data() {
    return {
        orders: null,
        configuration: null
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
    this.getAllOrders()
  },
  
  methods: {
    async getConfig() {
        this.configuration = await getConfiguration()
    },

    async getAllOrders() {
        try {
            const token = await getObject("token")
            
            const response = await axios.get(serverUrl + "/api/get-all-orders", {
                headers: {
                "Authorization": token 
                }
            });

            if (response && response.status === 200) {
                this.orders = response.data.data
            }
            
        } catch (error) {
            await removeObject("token")
            location.replace("/login")
        }
    },

    async refreshData() {
        await Haptics.impact()

        this.orders = null
        await this.getAllOrders()   
    },
  }

}
</script>