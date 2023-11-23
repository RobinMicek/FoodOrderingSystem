<template>
    
    <TopBar :backLink="'/menus?establishmentId=' + establishmentId" text="Vyberte Produkty"/>

    <div class="h-full flex flex-col items-center mx-5vw my-5vh">

        <div v-if="products && products.length != 0" class="w-full">
            <pull-to-refresh @refresh="refreshData">
                <div v-for="product in products">                    
                
                    <div class="mb-3vh relative h-full grid grid-cols-3 w-full bg-white rounded-lg">
                        
                        <div class="col-span-1">
                            <img
                                :src="serverUrl + product.imagePath"
                                class="w-full h-full object-cover rounded-tl-lg rounded-bl-lg"
                            />
                        </div>

                        <div class="col-span-2 p-2vh">                      
                            <h1 class="text-secondary font-medium">{{ product.name }}</h1>   
                            <h1 class="text-xs pb-2">{{ product.description }}</h1>                               
                                                                                    
                            <div class="text-right">
                                <button type="button" @click="this.addProductToCart(product)"
                                    class="bg-secondary text-white p-1vh text-sm rounded-lg ring-secondary font-medium">
                                    Přidat za {{ product.price }} Kč
                                </button>   
                            </div>                                         
                        </div>

                    </div>
                
                </div>
            </pull-to-refresh>
        </div>

        <div v-else-if="products && products.length === 0">
            <h1 class="text-lg text-center text-white">Nejsou dostupné žádné produkty!</h1>
        </div>

        <div v-else>
            <Loading />
        </div>
    
        <Cart :price="price" :numberOfProducts="numberOfProducts" :establishmentId="establishmentId"/>
    </div>

</template>


<script>
// Import Components
import TopBar from "@/components/TopBar.vue"
import Loading from "@/components/Loading.vue"
import Cart from "@/components/Cart.vue"
import PullToRefresh from "@/components/PullToRefresh.vue"

// Import Modules 
import axios from 'axios'
import { Haptics } from "@capacitor/haptics"

// Import JS
import { getObject, removeObject } from "@/utils/storage.js"
import { CartObject } from "@/utils/cart.js"

// Import Variables
import { serverUrl } from "@/variables.js"

export default {
  data() {
    return {
        serverUrl,
        products: null,
        establishmentId: null,

        price: 0,
        numberOfProducts: 0
    }
  },
  
  // Register Components
  components: {
    TopBar,
    Loading,
    Cart,
    PullToRefresh
  },

  mounted() {
    this.getAllMenus()
    this.cartLogic()
  },
  
  methods: {
    async getAllMenus() {
        try {
            const menuId = new URLSearchParams(window.location.search).get("menuId")
            const establishmentId = new URLSearchParams(window.location.search).get("establishmentId")
            this.establishmentId = establishmentId

            const token = await getObject("token")
            
            const response = await axios.get(serverUrl + "/api/get-menu?menuId=" + menuId, {
                headers: {
                "Authorization": token 
                }
            });

            if (response && response.status === 200) {
                this.products = response.data.data.products
            }
            
        } catch (error) {
            await removeObject("token")
            location.replace("/login")
        }
    },

    async cartLogic() {
        this.cartObject = new CartObject(this.establishmentId)   

        const stats = await this.cartObject.getStats()
        this.price = stats.price
        this.numberOfProducts = stats.numberOfProducts
    },

    async addProductToCart (product) {
        this.cartObject.addItem(product)
        
        // Update cart
        const stats = await this.cartObject.getStats()
        this.price = stats.price
        this.numberOfProducts = stats.numberOfProducts
    },

    async refreshData() {
        await Haptics.impact()

        this.products = null
        await this.getAllMenus()   
    }
  }

}
</script>