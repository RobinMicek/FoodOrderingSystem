<template>

    <span class="m-10vh"></span>

    <div class="fixed z-10 bottom-0 left-0 w-full">
        <div class="mx-5vw my-1vh  py-2vh px-3vh bg-secondary text-white rounded-md shadow-xl">
            <router-link :to="{ name: 'checkout', query: { establishmentId: establishmentId} }">
                <div class="grid grid-cols-3 gap-y-5">
                    
                    <div class="col-span-1 text-left pt-1.5">
                        <vue-feather type="shopping-cart" size="24" class=" "/>
                    </div>
                    <div class="col-span-1 text-center">
                        <h1 class="font-medium">{{ price }} Kč</h1>
                        <h1 class="text-xs">Cena</h1>
                    </div>
                    <div class="col-span-1 text-center">                    
                        <h1 class="font-medium">{{ numberOfProducts }}</h1>
                        <h1 class="text-xs">Počet Produktů</h1>
                    </div>
                </div>
            </router-link>                      
        </div>
    </div>

</template>


<script>
export default {
  props: {
    price: Number,
    numberOfProducts: Number,
    establishmentId: String
  }
}
</script>