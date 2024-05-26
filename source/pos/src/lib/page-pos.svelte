<script>
    // IMPORTS
    import { onMount } from "svelte";
    import { isMerchantCartSubmited } from "../utils/stores";

    // Import components
    import Cart from "./page-pos/cart.svelte"
    import Products from "./page-pos/products.svelte";

    // On load delete merchantCardNumber value -> Prevent asigning cards from refills
    onMount( () => {
        localStorage.removeItem("merchantCardNumber")
        isMerchantCartSubmited.set(false)
    } )
</script>


<main class="h-full w-full">
    <div class="h-full w-full grid grid-cols-10">
        <div class="h-full w-full col-span-6 xl:col-span-7">
            <Products/>
        </div>
    
        <div class="h-full w-full col-span-4 xl:col-span-3">
            <Cart/>
        </div>
    </div>
</main>