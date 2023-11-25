<template>
    <div v-if="type == 'home'">
        <div class="top-0 pt-2 px-2 w-screen bg-primary">

            <div class="pt-3">
                <router-link to="/navbar">
                    <vue-feather type="menu" size="36" class="pt-1 text-white"/>
                </router-link>  
            </div>

        </div>
    </div>
    

    <div v-else>      
        <div class="top-0 pt-2 px-2 w-screen bg-secondary">
            <div class="pt-3 flex items-center justify-start">

                <div class="">
                    <router-link :to="backLink" class="">
                        <a class="page-link">
                            <vue-feather type="arrow-left" size="36" class="pt-1 text-white"/>
                        </a>
                    </router-link> 
                </div>

                <div class="pl-2">
                    <h1 class="text-white text-xl font-medium">{{ text }}</h1>
                </div>
            </div>

        </div>
    </div>
</template>


<script>
// Import Components

// Import Modules

// Import JS

// Import Variables

export default {
    data() {
        return {
        }
    },

    props: {
        text: String,
        backLink: String,    
        type: String
    }
};
</script>
  