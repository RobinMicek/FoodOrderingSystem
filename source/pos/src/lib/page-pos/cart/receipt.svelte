<script>
    // IMPORTS
    import { createEventDispatcher } from "svelte";

    // Props
    export let orderId
    export let orderTag
    export let cart 
    export let paymentType
    export let isCardSubmited

    const establishmentName = localStorage.getItem("establishmentName")
    const establishmentId = localStorage.getItem("establishmentId")
    const companyName = localStorage.getItem("companyName")
    const companyAddress = localStorage.getItem("companyAddress")
    const companyPhone = localStorage.getItem("companyPhone")
    const companyCIN = localStorage.getItem("companyCIN")

    // Close modal
    const dispatch = createEventDispatcher()
</script>


<main>
    <div class="fixed inset-0 h-full w-full z-20 flex justify-center items-center backdrop-filter backdrop-blur-lg">
        
        <div class="print bg-white p-4 print:w-auto print:h-full w-3/12 h-4/5 overflow-y-scroll rounded-lg space-y-4">

            <!-- Print button-->
            <div class="no-print mb-10 flex w-full justify-between gap-4">
                <button on:click={ () => dispatch("closeReceiptModal") } class="w-full bg-red-500 hover:bg-transparent border-2 border-red-500 text-white hover:text-red-500 font-semibold text-lg rounded-lg p-2 2xl:p-4 uppercase">
                    <i class="las la-times"></i>
                    Zavřít
                </button>

                <button on:click={ () => window.print() } class="w-full bg-secondary hover:bg-transparent border-2 border-secondary text-white hover:text-secondary font-semibold text-lg rounded-lg p-2 2xl:p-4 uppercase">
                    <i class="las la-print"></i>
                    Vytisknout
                </button>
            </div>
           
            <div>
                
            </div>
            <!-- Logo -->
            <div class="flex w-full justify-center">
                <img src="favicon.png" alt="logo" class="h-24">
            </div> 
            
            <!-- Company info -->
            <div class="text-center">
                <h1 class="font-semibold text-xl mb-4">{ companyName }</h1>
                <h1 class="">{ companyAddress }</h1>
                <h1 class="">Telefon: <span class="font-semibold">{ companyPhone }</span></h1>
                <h1 class="">IČO: <span class="font-semibold">{ companyCIN }</span></h1>
                <h1 class="">{ establishmentName }</h1>
            </div>

            <!-- Order tag-->
            <hr>
            <div class="text-center">
                <h1 class="text-6xl font-bold">{ String(orderTag).padStart(3, '0') }</h1>
            </div>
            
            
            <!-- Datetime, receipt number-->
            <hr>
            <div class="">
                <h1 class="text-center">Číslo účtenky: <span class="font-semibold">{ establishmentId }-{ orderId }-{ Math.round(Math.random() * 1000)}</span></h1>
                <div class="flex w-full justify-between">
                    <h1>Datum: <span class="font-semibold">{ new Date().toLocaleDateString() }</span></h1>
                    <h1>Čas: <span class="font-semibold">{ new Date().toLocaleTimeString() }</span></h1>
                </div>
            </div>
            
            <!-- Products -->
            <hr>
            <div>
                {#each cart as { name, price, quantity }}
                    <div class="flex w-full justify-between items-center gap-4 my-1">
                        <h1 class="text-lg">{ quantity }x { name }</h1>
                        <h1 class="text-lg font-semibold text-nowrap">{ (price * quantity).toFixed(2) } Kč</h1>
                    </div>
                {/each}
            </div>
            
            <!-- Total price + payment info -->
            <hr>
            <div>
                <div class="flex w-full justify-between items-center gap-4 my-1">
                    <h1 class="text-xl">Celkem</h1>
                    <h1 class="text-xl font-semibold text-nowrap">{ Math.round(cart.reduce((total, item) => total + item.price * item.quantity, 0)) } Kč</h1>
                </div>
            
                <h1>Typ platby: <span class="font-semibold">{ paymentType == "WALLET" ? "Peněženka" : "Hotovost"}</span></h1>
                <h1>Zákaznická karta: <span class="font-semibold">{ isCardSubmited ? "Ano" : "Ne"}</span></h1>
            </div>
            
            
            <!-- Footer -->
            <hr>
            <div class="text-center">
                <h1>Zpracoval objednávkový systém <span class="font-semibold">K Okénku</span></h1>
            </div>

        </div>
        
        
    </div>
</main>