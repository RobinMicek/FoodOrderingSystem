<script>
    // IMPORTS
    import { completeOrder } from "../../utils/serverRequests";

    // Import components
    import Item from "./cart/item.svelte"
    import SubmitCard from "./cart/submitCard.svelte";
    import Receipt from "./cart/receipt.svelte";

    // Cart store
    import { cart, isMerchantCartSubmited } from "../../utils/stores";
    let currentCart
    cart.subscribe((value => {
        currentCart = value
    }))


    // Submit card
    let showSubmitCardModal = false
    function handleCloseSubmitCardModal (event) {
        showSubmitCardModal = event.detail
    }

    let isCardSubmited = false
    isMerchantCartSubmited.subscribe((value => {
        isCardSubmited = value
    }))


    // Submit order 
    let isOrderCompleted = false
    let orderTag
    let orderId
    let paymentType
    async function submitOrder (selectedPaymentType) {
        paymentType = selectedPaymentType
        isOrderCompleted = true
        const response = await completeOrder(currentCart, selectedPaymentType)

        if (response != false) {
            orderId = response.orderId
            orderTag = response.tag
        } else {
            alert("Něco se nepovedlo!")
            cleanUp()
        }

    }


    // Close modal receipt => clean up
    function cleanUp () {
        localStorage.removeItem("merchantCardNumber")
        isMerchantCartSubmited.set(false)
        isOrderCompleted = false

        cart.set([])

        orderId = null
        orderTag = null
    }
</script>

<main class="h-full w-full">
    
    <!-- Submit card -->
    {#if showSubmitCardModal }
        <SubmitCard on:closeSubmitCardModal={ handleCloseSubmitCardModal }/>
    {/if}


    <!-- Receipt --> 
    {#if orderId && orderTag }
        <Receipt on:closeReceiptModal={ cleanUp } cart={ currentCart } orderId={ orderId } orderTag={ orderTag } paymentType={ paymentType } isCardSubmited={ isCardSubmited } />
    {/if}


    <div class="w-full h-full flex flex-col bg-white rounded-lg p-3">
        
        <div class="justify-center px-2 flex w-full">
            <h1 class="font-semibold text-2xl uppercase">Účet</h1>
        </div>
        
        <!-- Is card Submited -->
        {#if isCardSubmited }
            <div class="bg-violet-500 text-white text-center rounded-lg p-4 my-1 w-full flex items-center justify-between">
                <h1 class="text-xl">
                    <i class="las la-wallet"></i>
                </h1>
                <h1 class="text-white font-semibold text-lg uppercase">
                    Karta načtena
                </h1>
            </div>
        {/if}
        
        <!-- Cart items -->
        <div class="overflow-y-scroll flex-grow h-32">
            {#each currentCart as { productId, quantity, name, price } }
                <Item  name={ name } quantity={ quantity } price={ price }/>
            {/each}
        </div>
        
        <div class="">
            <!-- Total price -->
            <div class="bg-zinc-500 flex justify-between items-center rounded-lg p-4 my-1">
                <h1 class="text-white font-semibold text-xl uppercase">Celkem</h1>
                <h1 class="text-white font-semibold text-xl">{ Math.round(currentCart.reduce((total, item) => total + item.price * item.quantity, 0)) } Kč</h1>
            </div>

            <!-- Control buttons -->
            <div class="grid grid-cols-4 gap-2 mt-2">

                <button on:click={ () => showSubmitCardModal = true } class="aspect-square rounded-lg bg-lime-600 hover:bg-transparent border-2 border-lime-600 text-white hover:text-lime-600 p-2 2xl:p-4 space-y-1">
                    <i class="las la-qrcode text-2xl xl:text-4xl"></i>
                    <h1 class="font-semibold uppercase">Karta</h1>
                </button>

                <button class="aspect-square rounded-lg bg-amber-500 text-white p-2 2xl:p-4 space-y-1" disabled>
                    <i class="las la-chair text-2xl xl:text-4xl"></i>
                    <h1 class="font-semibold uppercase">Stůl</h1>
                </button>

                <button on:click={ cleanUp } class="aspect-square rounded-lg bg-red-500 hover:bg-transparent border-2 border-red-500 text-white hover:text-red-500 p-2 2xl:p-4 space-y-1">
                    <i class="las la-redo-alt text-2xl xl:text-4xl"></i>
                    <h1 class="font-semibold uppercase">Storno</h1>
                </button>

                <button class="aspect-square rounded-lg bg-slate-500 text-white p-2 2xl:p-4 space-y-1" disabled>
                    <i class="las la-lock text-2xl xl:text-4xl"></i>
                    <h1 class="font-semibold">ODHLÁSIT</h1>
                </button>

            </div>

            <!-- Payment buttons -->
            <div class="mt-2 flex gap-2">
                <button on:click={ () => submitOrder("WALLET") } disabled={ !isCardSubmited || isOrderCompleted } class="text-white hover:text-sky-500 disabled:hover:text-white bg-sky-500 border-sky-500 disabled:border-zinc-500 hover:bg-transparent disabled:bg-zinc-500 font-semibold flex w-full justify-between items-center border-2 rounded-lg p-3 my-1">
                    <i class="las la-wallet text-2xl xl:text-4xl"></i>
                    <h1 class="font-semibold text-xl uppercase">Karta</h1>
                </button>

                <button on:click={ () => submitOrder("CASH") } disabled={ isOrderCompleted } class="text-white hover:text-blue-500 disabled:hover:text-white font-semibold bg-blue-500 disabled:bg-zinc-500 hover:bg-transparent border-2 border-blue-500 disabled:border-zinc-500 flex w-full justify-between items-center rounded-lg p-3 my-1">
                    <i class="las la-coins text-2xl xl:text-4xl"></i>
                    <h1 class="font-semibold text-xl uppercase">Hotovost</h1>
                </button>
            </div>
        </div>

    </div>
</main>