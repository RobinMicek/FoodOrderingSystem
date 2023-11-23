<template>
    <div class="h-screen overflow-hidden">

        <TopBar type="home"/>
        
        <div class="mx-5vw mt-10vh flex justify-center">
            <img src="@/assets/images/logo.png" class="w-2/3">
        </div>


        <div class="absolute bottom-0 left-0 right-0">
            <div class="m-5vw">
                <router-link to="/establishments">
                    <div class="h-10vh mb-5vh bg-secondary rounded-xl hover:bg-primary hover:ring-2 hover:ring-secondary text-white hover:text-white">
                        <div class="flex items-center justify-center h-full gap-2">
                            <vue-feather type="credit-card" size="36"/>
                            <div class="text-center">
                                <h1 class="text-xl font-medium">OBJEDNAT</h1>
                            </div>
                        </div>                    
                    </div>
                </router-link>

        
                <div class="grid grid-cols-2 gap-5vw w-full">
                    <router-link to="/establishments-list">
                        <div class="relative w-full h-10vh">
                            <div class="absolute inset-0 bg-white rounded-xl hover:bg-primary hover:ring-2 hover:ring-white text-text hover:text-white">
                                <div class="flex items-center justify-center h-full gap-2">
                                    <vue-feather type="home" size="36"/>
                                    <div class="text-center">
                                        <h1 class="text-md font-medium">Provozovny</h1>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </router-link>                    

                    <router-link to="/orders">
                        <div class="relative w-full h-10vh">
                            <div class="absolute inset-0 bg-white rounded-xl hover:bg-primary hover:ring-2 hover:ring-white text-text hover:text-white">
                                <div class="flex items-center justify-center h-full gap-2">
                                    <vue-feather type="shopping-cart" size="36"/>
                                    <div class="text-center">
                                        <h1 class="text-md font-medium">Objednávky</h1>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </router-link>

                </div>
            </div>
        </div>
    </div>
</template>


<script>
// Import Components
import TopBar from "@/components/TopBar.vue"

// Import Modules 

// Import JS

// Import Variables

export default {
  // Register Components
  components: {
    TopBar
  }
}
</script>