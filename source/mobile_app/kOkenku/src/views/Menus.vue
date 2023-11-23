<template>
    
    <TopBar backLink="/establishments" text="Vyberte Menu"/>

    <div class="h-full flex flex-col items-center mx-5vw my-5vh">
    
        <div v-if="menus && menus.length != 0" class="w-full">
            <pull-to-refresh @refresh="refreshData">
                <div v-for="menu in menus">                    
                
                    <router-link :to="{ name: 'products', query: { establishmentId: establishmentId, menuId: menu.menuId } }">
                        <div class="mb-3vh relative min-h-full grid grid-cols-3 w-full bg-white rounded-lg">
                            
                            <div class="col-span-1">
                                <img :src="serverUrl + menu.imagePath" class="h-full w-full object-cover rounded-tl-lg rounded-bl-lg">
                            </div>

                            <div class="col-span-2 p-2vh">                      
                                <h1 class="text-secondary font-medium">{{ menu.name }}</h1>   
                                <h1 class="text-xs">{{ menu.description }}</h1>                      
                            </div>

                        </div>
                    </router-link>
                
                </div>
            </pull-to-refresh>
        </div>

        <div v-else-if="menus && menus.length === 0">
            <h1 class="text-lg text-center text-white">Nejsou dostupná žádná menu!</h1>
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
        menus: null,
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
            const establishmentId = new URLSearchParams(window.location.search).get("establishmentId")
            this.establishmentId = establishmentId

            const token = await getObject("token")
            
            const response = await axios.get(serverUrl + "/api/get-establishment?establishmentId=" + establishmentId, {
                headers: {
                "Authorization": token 
                }
            });

            if (response && response.status === 200) {
                this.menus = response.data.data.menus
            }
            
        } catch (error) {
            await removeObject("token")
            location.replace("/login")
        }
    },

    async cartLogic() {
        this.cartObject = new CartObject(this.establishmentId)     

        let stats = await this.cartObject.getStats()
        this.price = stats.price
        this.numberOfProducts = stats.numberOfProducts
    },

    async refreshData() {
        await Haptics.impact()

        this.menus = null
        await this.getAllMenus()   
    }
  }

}
</script>