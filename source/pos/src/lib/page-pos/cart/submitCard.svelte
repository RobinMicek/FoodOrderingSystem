<script>
    // IMPORTS
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher()

    // Import merchantCardStatus store
    import { isMerchantCartSubmited } from "../../../utils/stores";

    let cardNumber = localStorage.getItem("merchantCardNumber")

    function closeModal() {
        dispatch("closeSubmitCardModal", false)
    }

    function storeCardNumber () {
        localStorage.setItem("merchantCardNumber", cardNumber)
        isMerchantCartSubmited.set(true)
        closeModal()
    }

    function deleteCardNumber () {
        localStorage.removeItem("merchantCardNumber")
        isMerchantCartSubmited.set(false)
        closeModal()
    }
</script>


<main>
    <div class="fixed inset-0 h-full w-full z-20 flex justify-center items-center backdrop-filter backdrop-blur-lg">
        
        <div class=" bg-white p-4 w-1/2 2xl:w-1/4 rounded-lg space-y-4">
            <div class="bg-secondary text-center rounded-lg p-4 my-1">
                <h1 class="text-white font-semibold text-xl uppercase">Uživatelská karta</h1>
            </div>
    
            <div>
                <input type="text" bind:value={ cardNumber } placeholder="Karta-6db3b89e-178d-11ef-bdbf-0242ac110002" class="w-full p-4 rounded-lg border-2 border-zinc-500">
            </div>
    
            <div class="flex justify-between gap-2">
                <button on:click={ deleteCardNumber } class="w-full bg-red-500 hover:bg-transparent border-2 border-red-500 text-white hover:text-red-500 font-semibold text-lg rounded-lg p-4 uppercase">
                    <i class="las la-trash"></i>
                    Smazat
                </button>
                
                <button on:click={ closeModal } class="w-full bg-zinc-500 hover:bg-transparent border-2 border-zinc-500 text-white hover:text-zinc-500 font-semibold text-lg rounded-lg p-4 uppercase">
                    <i class="las la-times"></i>
                    Zavřít
                </button>
                
                <button on:click={ storeCardNumber } class="w-full bg-green-600 hover:bg-transparent border-2 border-green-600 text-white hover:text-green-600 font-semibold text-lg rounded-lg p-4 uppercase">
                    <i class="las la-check"></i>
                    Uložit
                </button>
            </div>
        </div>
        
        
    </div>
</main>