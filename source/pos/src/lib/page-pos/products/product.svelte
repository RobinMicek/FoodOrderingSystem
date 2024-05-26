<script>
    // IMPORTS

    let serverUrl = localStorage.getItem("urlServer")

    // Cart store
    import { cart } from "../../../utils/stores";
    let currentCart
    cart.subscribe((value => {
        currentCart = value
    }))

    function addToCart (productId) {
        if (currentCart[currentCart.findIndex(item => item.productId == productId)] != undefined) {
            currentCart[currentCart.findIndex(item => item.productId == productId)].quantity++
        } else {
            currentCart.push({"productId": productId, "quantity": 1, "name": name, "price": price, "preparationTime": preparationTime })
        }
        cart.set(currentCart)
    }


    // Props
    export let name
    export let price
    export let imagePath
    export let productId
    export let preparationTime
</script>


<main>
    <button on:click={() => addToCart(productId=productId)} class="rounded-lg aspect-square overflow-hidden h-full relative shadow-lg border-2 border-transparent hover:border-secondary">
        <img src={ serverUrl + imagePath } alt="Náhledový obrázek" class="object-cover rounded-lg w-full h-full">
        
        
        <div class="bg-secondary bg-opacity-90 text-white right-0 absolute top-0 z-10 p-4 rounded-bl-lg">
            <h1 class="font-bold text-2xl text-nowrap">{ price } Kč</h1>
        </div>
        
        <div class="bg-primary bg-opacity-75 w-full absolute bottom-0 z-10 p-2">
            <h1 class="font-semibold text-white">{ name }</h1>
        </div>
    </button>
</main>