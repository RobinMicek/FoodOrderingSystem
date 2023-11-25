<template>
    
    <TopBar backLink="/" :text="appName"/>

    <div class="h-full flex flex-col items-center gap-y-3vh mx-5vw my-5vh">

        <div v-for="button in buttons" class="w-full">
            <router-link :to="button.link" class="w-full">
                <button
                    class="bg-white text-primary w-full p-2vh text-lg rounded-lg focus:ring-2 focus:text-white focus:bg-primary ring-white focus:outline-none">
            
                    <div class="flex items-center justify-left w-full h-full gap-2">                
                        <vue-feather :type="button.icon" size="24" class=" "/>
                        {{ button.text }}
                    </div>
                </button>
            </router-link>
        </div>

    </div>
    
</template>


<script>
// Import Components
import TopBar from "@/components/TopBar.vue"

// Import Modules 

// Import JS

// Import Variables
import { appName } from "@/variables.js"

export default {
  data() {
    return {
        appName,
        buttons: [
            {
                "text": "Moje Objednávky",
                "link": "/orders",
                "icon": "shopping-cart"
            },
            {
                "text": "Provozovny",
                "link": "/establishments-list",
                "icon": "home"
            },
            {
                "text": "Obchodní Podmínky",
                "link": "/terms",
                "icon": "file-text"
            },
            {
                "text": "Kontakt",
                "link": "/contact",
                "icon": "phone"
            },
            {
                "text": "Odhlásit Se",
                "link": "/logout",
                "icon": "log-out"
            },
            {
                "text": "Test",
                "link": "/test",
                "icon": "log-out"
            }
        ]
    }
  },
  
  // Register Components
  components: {
    TopBar
  }
}
</script>