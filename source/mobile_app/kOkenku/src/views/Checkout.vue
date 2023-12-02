<template>
    
    <TopBar :backLink="'/menus?establishmentId=' + establishmentId" text="Košík"/>

    <!-- Pay and Order PopUp Info -->
    <div v-if="payAndOrder" class="fixed z-10 bottom-0 left-0 w-full">
        <div class="mx-5vw py-2vh pb-20vh px-3vh bg-secondary text-white text-center rounded-tl-lg rounded-tr-lg shadow-xl">
            <div>
                <button @click="togglePayAndOrder" class="absolute right-0 mr-5vw pr-5">
                    <vue-feather type="x" size="24" class="text-red-500"/>
                </button>
            </div>  

            <h1 class="font-medium text-xl border-b-2">Informace k Platbě</h1>
            <p class="mt-3 text-sm">
                Protože je tento projekt maturitní práce, tak není napojen na žádnou platební bránu. 
                <br><br>
                V ostrém provozu byste nyní byli vyzváni k zadání údajů z karty 
                nebo mohli využít bezpečné platební metody jako <b>Apple Pay <sup>TM</sup></b> nebo <b>Google Pay<sup>TM</sup></b>.
                <br><br>
                Děkuji za pochopení.
            </p>

            <div class="mt-10">
                <button @click="completeOrder"
                    class="flex items-center justify-center gap-3 p-2 w-full bg-primary rounded-md text-white text-lg font-medium">
                    <vue-feather type="credit-card" size="24"/>
                    Objednat
                </button>
            </div>
        </div>
    </div>
    
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
                                <th class="px-1 py-1">Cena</th>
                                <th class="px-1 py-1"></th>
                            </tr>
                        </thead>
                        <tbody v-for="product in products">                            
                            <tr>
                                <td class="px-1 py-1.5">{{ product.quantity}}x {{ product.name}}</td>
                                <td class="px-1 py-1.5">{{ (product.price * product.quantity).toFixed(2) }}</td>
                                
                                <td v-if="deleteItemsFromCart" class="px-1 py-1.5">
                                    <button type="button" @click="removeItem(product.productId)">
                                        <vue-feather type="x" size="16" class="pt-1 text-red-500"/>
                                    </button>
                                </td>
                                <td v-else class="px-1 py-1.5">
                                    <button disabled>
                                        <vue-feather type="x" size="16" class="pt-1 text-gray-400"/>
                                    </button>
                                </td>
                            </tr>                  
                        </tbody>
                        <tfoot>
                            <tr class="border-t-2 border-white">                                
                                <td class="px-1 py-2 font-medium">Celkem</td>
                                <td class="px-1 py-2 font-medium whitespace-nowrap">{{ totalPrice }}Kč</td>
                            </tr>     
                        </tfoot>
                    </table>
                </div>
            </div>

            
            <div v-if="pickupTimeDetails">                
                <div class="mt-10 m-5vw grid grid-cols-3 text-white">
                    <div class="col-span-2">
                        <h1 class="text-xl font-medium p-2">Čas vyzvednutí</h1>
                    </div>

                    <div class="col-span-1">
                        <input type="time" id="pickupTime" v-model="pickupTime" :min="pickupTimeDetails.earliestPickupTime" :max="pickupTimeDetails.latestPickupTime" step="60" @input="validatePickupTime"
                            class="text-primary bg-white p-2 rounded-lg">
                    </div>
                </div>
                
                <div class="mt-10 p-2 m-3vw">
                    <button @click="togglePayAndOrder"
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
import { scheduleNotification  } from "@/utils/localNotifications"

// Import Variables
import { serverUrl, getConfiguration } from "@/variables.js"
import { withCtx } from "vue"

export default {
  data() {
    return {
        serverUrl,
        products: null,

        establishmentId: new URLSearchParams(window.location.search).get("establishmentId"),
        establishment: null,

        pickupTimeDetails: null,
        pickupTime: null,
        totalPrice: 0,
        configuration: null,    

        payAndOrder: false,
        deleteItemsFromCart: true
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
        
    },

    validatePickupTime() {
      const { earliestPickupTime, latestPickupTime } = this.pickupTimeDetails
      const selectedTime = this.pickupTime
      
      if ( selectedTime < earliestPickupTime || selectedTime > latestPickupTime)  {        
        this.pickupTime = earliestPickupTime;
      }
    },

    togglePayAndOrder() {
        if (this.payAndOrder === false) {
            this.deleteItemsFromCart = false // Disable the ability to delete items from cart
            this.payAndOrder = true    
        } else {
            this.deleteItemsFromCart = true
            this.payAndOrder = false    
        }
    },

    async completeOrder() {
        try {
            const token = await getObject("token")

            const headers = {
                'Content-Type': 'application/json',
                'Authorization': token
            }

            const data = {
                "establishmentId": parseInt(this.establishmentId),
                "pickupTime": this.pickupTime,
                "products": this.products
            }
            
            const response = await axios.post(serverUrl + "/api/create-order",            
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