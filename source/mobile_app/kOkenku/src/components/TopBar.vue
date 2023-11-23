<template>
    <div v-if="type == 'home'">
        <div class="top-0 h-7vh pt-2 px-2vw w-screen flex items-center bg-primary">
            <div class="absolute left-0 m-1">
                <router-link to="/navbar">
                    <vue-feather type="menu" size="36" class="pt-1 text-white"/>
                </router-link>            
            </div>
        </div>
    </div>
    

    <div v-else>        
        <div class="top-0 pt-2 px-2vw w-screen flex justify-start items-center bg-secondary">
            <div>
                <router-link :to="backLink" class="">
                    <a class="page-link">
                        <vue-feather type="arrow-left" size="36" class="pt-1 text-white"/>
                    </a>
                </router-link>
            </div>

            <div class="flex w-screen items-center justify-center text-center">
                <h1 class="text-white text-xl font-medium">{{ text }}</h1>
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
  