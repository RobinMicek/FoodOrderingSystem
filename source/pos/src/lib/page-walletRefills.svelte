<script>
    // IMPORTS
    import { getWallet, refillWallet } from "../utils/serverRequests";
    import { isMerchantCartSubmited } from "../utils/stores";
    import { onMount } from "svelte";

    // Import components
    import SubmitCard from "./page-pos/cart/submitCard.svelte";

    let refillAmount = ""
    let numbers = Array.from({ length: 9 }, (_,i) => i + 1 )
    let currentBalance = null

    // Submit card
    let showSubmitCardModal = false
    function handleCloseSubmitCardModal (event) {
        showSubmitCardModal = event.detail
    }

    let isCardSubmited = false
    isMerchantCartSubmited.subscribe((value => {
        isCardSubmited = value
    }))


    // Refill wallet
    async function handleWalletRefill () {
        await refillWallet(refillAmount)
        refillAmount = ""
        currentBalance = null
    }


    // On load delete merchantCardNumber value -> Prevent asigning cards from refills
    onMount( () => {
        localStorage.removeItem("merchantCardNumber")
        isMerchantCartSubmited.set(false)
    } )
</script>

<main class="flex w-full h-full justify-center items-center">

    <div class="w-full grid grid-cols-2 px-4">

        <div class="col-span-1 flex w-full flex-col items-center">
            <div class="w-96 space-y-12">
                <div class="space-y-4">

                    {#if isCardSubmited }
                        <div class="bg-green-500 text-white text-center rounded-lg p-4 my-1 flex items-center justify-center">
                            <h1 class="text-white font-semibold text-xl uppercase">
                                <i class="las la-check"></i>
                                Karta načtena
                            </h1>
                        </div>
                    {:else}
                    <div class="bg-red-500 text-white text-center rounded-lg p-4 my-1 flex items-center justify-center">
                        <h1 class="text-white font-semibold text-xl uppercase">
                            <i class="las la-times"></i>
                            Karta nenačtena
                        </h1>
                    </div>
                    {/if}


                    <div>
                        {#if showSubmitCardModal }
                            <SubmitCard on:closeSubmitCardModal={ handleCloseSubmitCardModal }/>
                        {:else}
                            <button on:click={ async () => showSubmitCardModal = true } class="font-semibold text-white border-2 p-4 w-full border-secondary hover:bg-transparent bg-secondary text-lg uppercase rounded-lg"> 
                                <i class="las la-credit-card"></i> 
                                Načíst Kartu
                            </button>
                        {/if}
                    </div>
                </div>
                    <hr>

                <div class="space-y-4">
                    <div>
                        <h1 class="text-white text-lg font-semibold ">Aktuální Zůstatek</h1>
                        <input value={ currentBalance != null && currentBalance != undefined && currentBalance != false ?  currentBalance + " Kč" : "Zůstatek nebyl zjištěn!"} type="text" class="w-full p-4 rounded-lg border-2 border-secondary bg-transparent text-white font-semibold text-right" disabled>
                    </div>
                    
                    <div>
                        <button on:click={ async () => currentBalance = (await getWallet()).walletBalance } class="font-semibold text-white border-2 p-4 w-full border-secondary hover:bg-transparent bg-secondary text-lg uppercase rounded-lg"> 
                            <i class="las la-wallet"></i> 
                            Zjistit Zůstatek
                        </button>
                    </div>
                </div>

            </div>

        </div>
      
        <div class="col-span-1 flex flex-col justify-center items-center w-full h-full">
            <div class="bg-secondary text-center rounded-t-lg p-4 w-96">
                <h1 class="text-white font-semibold text-xl uppercase">Dobíjení Peněženky</h1>
            </div>

            <div class="relative w-96">
                <input bind:value={ refillAmount } type="text" name="pin" id="preview" class="bg-white text-primary p-5 text-4xl text-center w-full h-20" disabled>
                <button type="button" on:click={ () => refillAmount = refillAmount.slice(0, -1) } class="absolute right-5 pt-5 z-10">
                    <i class="las la-backspace text-primary text-4xl"></i>
                </button>            
            </div>
    
            <div class="grid grid-cols-3">
                {#each numbers as number }
                    <div class="col-span-1 w-32 ">
                        
                        <button type="button" on:click={ () => refillAmount += number } class="bg-white text-primary p-5 w-full">
                            <h1 class="text-4xl">{ number }</h1>                        
                        </button>
                    
                    </div>
                {/each}
            </div>
            <div class="w-96">
                        
                <button on:click={ () => refillAmount += 0 } type="button" class="bg-white text-primary p-5 w-full">
                    <h1 class="text-4xl">0</h1>                        
                </button>
            
            </div>
    
            <div class="w-96">
                <button disabled={ !isCardSubmited } on:click={ handleWalletRefill } class="w-full bg-secondary disabled:bg-red-500 disabled:hover:bg-red-500 hover:bg-transparent border-2 disabled:border-red-500 border-secondary text-white hover:text-white-600 font-semibold text-lg rounded-b-lg p-4 uppercase">
                    <i class="las la-coins"></i>
                    Dobít Peněženku
                </button>
            <div>
        </div>

    </div>

</main>