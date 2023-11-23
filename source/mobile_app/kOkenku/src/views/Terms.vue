<template>
    
    <TopBar backLink="/" text="Obchodní Podmínky"/>

    <div class="h-full flex flex-col items-center mx-5vw my-5vh">

        <div v-if="terms && terms.length != 0">
            {{ terms }}
            <div v-html="terms" class="text-white" raw></div>
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

// Import Variables
import { serverUrl } from "@/variables.js"

export default {
  data() {
    return {
        serverUrl,
        terms: null,
    }
  },
  
  // Register Components
  components: {
    TopBar,
    Loading
  },

  mounted() {
    this.getTerms()
  },
  
  methods: {
    async getTerms() {
        
        const response = await axios.get(serverUrl + "/files/storage/texts/terms-of-service.txt")

        if (response && response.status === 200) {
            this.terms = response.data
        }
    }
  }

}
</script>