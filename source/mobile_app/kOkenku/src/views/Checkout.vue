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
    
    <TopBar :backLink="'/menus?establishmentId=' + establishmentId" text="Košík"/>

    
    <div class="h-full flex flex-col items-center mx-5vw my-5vh">

        <div v-if="products && products.length != 0 && establishment && configuration" class="w-full">
            
            <div class="text-center">
                <h1 class="font-medium text-2xl text-white">{{ establishment.name }}</h1>
            </div>

            <div class="mt-20 m-3vw text-white">

                <div class="w-full text-left text-sm">
                    <table class="min-w-full table-auto">
                        <thead>
                            <tr>
                                <th class="px-1 py-1">Produkt</th>
                                <th class="px-1 py-1 text-right">Cena</th>
                                <th class="px-1 py-1"></th>
                            </tr>
                        </thead>
                        <tbody v-for="product in products">                            
                            <tr>
                                <td class="px-1 py-1.5">{{ product.quantity}}x {{ product.name}}</td>
                                <td class="px-1 py-1.5 text-right">{{ (product.price * product.quantity).toFixed(2) }}</td>
                                
                                <td v-if="!payAndOrder" class="px-1 py-1.5 text-right">
                                    <button type="button" @click="removeItem(product.productId)">
                                        <vue-feather type="x" size="16" class="pt-1 text-red-500"/>
                                    </button>
                                </td>
                                <td v-else class="px-1 py-1.5 text-right">
                                    <button disabled>
                                        <vue-feather type="x" size="16" class="pt-1 text-gray-400"/>
                                    </button>
                                </td>
                            </tr>                  
                        </tbody>
                        <tfoot>
                            <tr class="border-t-2 border-white">                                
                                <td class="px-1 py-2 font-medium">Celkem</td>
                                <td class="px-1 py-2 font-medium text-right whitespace-nowrap">{{ totalPrice }} Kč</td>
                            </tr>     
                        </tfoot>
                    </table>
                </div>
            </div>

            
            <div v-if="pickupTimeDetails">                
                <div class="mt-10 m-5vw text-white">
                    <div>
                        <h1 class="font-semibold">Čas Vyzvednutí</h1>
                        <input type="time" id="pickupTime" v-model="pickupTime" :min="pickupTimeDetails.earliestPickupTime" :max="pickupTimeDetails.latestPickupTime" step="60" @input="validatePickupTime"
                            class="text-primary bg-white p-2 rounded-lg w-full h-12">
                        
                        <br>
                        <br>

                        <h1 class="font-semibold">Typ Platby</h1>
                        <select id="paymentType" v-model="paymentType"
                            class="text-primary bg-white p-2 rounded-lg w-full h-12">

                                <option value="WALLET">PENĚŽENKA</option>
                        </select>
                    </div>
                </div>
                
                <div v-if="payAndOrder" class="mt-10 p-2 m-3vw">
                    <button @click="completeOrder"
                        class="flex items-center justify-center gap-3 p-2 w-full bg-secondary rounded-md text-white text-lg font-medium">
                        <vue-feather type="credit-card" size="24"/>
                        Zaplatit a Objednat
                    </button>
                </div>
            </div>
            <div v-else-if="pickupTimeDetails === false" class="mt-10 m-5vw text-white text-center">
                <p>Objednávku není možné dokončit, doba přípravy některých produktů překračuje otevírací dobu provozovny.</p>
            </div>

            <div v-else>
                <button @click="getPickupTimeWindow"
                    class="mt-10 p-2 m-3vw w-full bg-secondary rounded-md text-white text-lg font-medium">Pokračovat</button>
            </div>
        
        </div>

        <div v-else-if="products && products.length === 0">
            <h1 class="text-lg text-center text-white">Nevybrali jste žádné produkty!</h1>
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

// Import Modules 
import axios from 'axios'

// Import JS
import { getObject, removeObject } from "@/utils/storage.js"
import { CartObject } from "@/utils/cart.js"
import { checkForPickupTimeWindow } from "@/utils/pickupTime.js"
import { scheduleNotification } from "@/utils/localNotifications"

// Import Variables
import { serverUrl, getConfiguration } from "@/variables.js"

export default {
  data() {
    return {
        serverUrl,
        products: null,

        establishmentId: new URLSearchParams(window.location.search).get("establishmentId"),
        establishment: null,

        paymentType: "WALLET",
        pickupTimeDetails: null,
        pickupTime: null,
        totalPrice: 0,
        configuration: null,    

        payAndOrder: false,
        orderCompleted: false
    }
  },
  
  // Register Components
  components: {
    TopBar,
    Loading
  },

  mounted() {
    this.getConfig(),
    this.getEstablishment()
    this.getProducts(),
    this.getPrice()
  },
  
  methods: {
    async getConfig() {
        this.configuration = await getConfiguration()
    },

    async getEstablishment() {
        try {
            const token = await getObject("token")
            
            const response = await axios.get(serverUrl + "/api/get-establishment?establishmentId=" + this.establishmentId, {
                headers: {
                "Authorization": token 
                }
            });

            if (response && response.status === 200) {
                this.establishment = response.data.data
            }
            
        } catch (error) {
            await removeObject("token")
            location.replace("/login")
        }
    },

    async getProducts() {
        this.cartObject = new CartObject(this.establishmentId)


        const cart = await this.cartObject.getCart()
        this.products = cart.products

        return this.products
    },

    async getPrice() {
        const stats = await this.cartObject.getStats()
        this.totalPrice = stats.price
    },

    async removeItem(productId) {
        await this.cartObject.removeItem(productId)

        // Update cart
        const cart = await this.cartObject.getCart()
        this.products = cart.products

        const stats = await this.cartObject.getStats()
        this.totalPrice = stats.price

        // Update pickup time window
        await this.getPickupTimeWindow()
    },

    async getPickupTimeWindow() {        
        const response = await checkForPickupTimeWindow(this.establishmentId)

        this.pickupTime = response.earliestPickupTime
        this.pickupTimeDetails = response

        this.deleteItemsFromCart = false
        this.payAndOrder = true
        
    },

    validatePickupTime() {
      const { earliestPickupTime, latestPickupTime } = this.pickupTimeDetails
      const selectedTime = this.pickupTime
      
      if ( selectedTime < earliestPickupTime || selectedTime > latestPickupTime)  {        
        this.pickupTime = earliestPickupTime;
      }
    },

    async completeOrder() {
        try {
            if (this.orderCompleted === false) {
                this.orderCompleted = true

                const token = await getObject("token")

                const headers = {
                    'Content-Type': 'application/json',
                    'Authorization': token
                }

                const data = {
                    "cardNumber": await getObject("cardNumber"),
                    "paymentType": this.paymentType,
                    "establishmentId": parseInt(this.establishmentId),
                    "pickupTime": this.pickupTime,
                    "products": this.products
                }
                
                const response = await axios.post(serverUrl + "/api/create-order-user",            
                    data,
                    { headers }
                );

                if (response && response.status === 200) {
                    await this.cartObject.cleanCart()

                    // Schedule local notification
                    if (this.configuration.app.showLocalNotifications === true) {

                        // Make date object out of pickupTime
                        const notifyDate = new Date()
                        const [hours, minutes] = this.pickupTime.split(':').map(Number)
                        notifyDate.setHours(hours, minutes, 0, 0)

                        // Create notification
                        const notification = await scheduleNotification(notifyDate)
                    }

                    location.replace("/order?orderId=" + response.data.data.orderId)
                }
            } else {
                alert("Něco se pokazilo! Prosím zkuste opakovat objednávku znovu později.")
                location.replace("/")
            }
            
            
        } catch (error) {
            // await removeObject("token")
            console.log(error)
            await this.cartObject.cleanCart()
            alert("Něco se pokazilo! Prosím zkuste opakovat objednávku znovu později.")
            location.replace("/")
            
        }
    }
   
  }

}
</script>