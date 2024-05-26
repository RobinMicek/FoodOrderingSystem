<script>
    // IMPORTS

    let urlServer = localStorage.getItem("urlServer")
    let apiToken = localStorage.getItem("apiToken")
    let urlKitcheHub = localStorage.getItem("urlKitchenHub")
    let kitchenHubShowPage = localStorage.getItem("kitchenHubShowPage")

    function storeValues () {
        localStorage.setItem("urlServer", urlServer)
        localStorage.setItem("apiToken", apiToken)
        localStorage.setItem("urlKitchenHub", urlKitcheHub)
        localStorage.setItem("kitchenHubShowPage", kitchenHubShowPage)

        alert("Hodnoty byly uloženy!")
    }

</script>

<main class="">
   
    <div class="space-y-4">
        <div>
            <h1 class="text-white text-lg font-semibold">Server - URL Adresa</h1>
            <input bind:value={ urlServer } type="url" class="w-full p-4 rounded-lg border-2 border-secondary bg-transparent text-white">
        </div>
    
        <div>
            <h1 class="text-white text-lg font-semibold">API Token</h1>
            <input bind:value={ apiToken } type="text" class="w-full p-4 rounded-lg border-2 border-secondary bg-transparent text-white">
        </div>
    
        <div>
            <h1 class="text-white text-lg font-semibold">KitchenHub - URL Adresa</h1>
            <input bind:value={ urlKitcheHub } type="url" class="w-full p-4 rounded-lg border-2 border-secondary bg-transparent text-white">
        </div>
        
        <div>
            <h1 class="text-white text-lg font-semibold">KitchenHub - Mód</h1>
            <select bind:value={ kitchenHubShowPage } class="w-full p-4 rounded-lg border-2 border-secondary bg-transparent text-white">
                <option value="kitchen-collect" class="text-black">Kitchen / Collect</option>
                <option value="collect-point" class="text-black">Collect Point</option>
            </select>
        </div>


        <div>
            <button on:click={ storeValues } class="w-full bg-secondary hover:bg-transparent border-2 border-secondary text-white hover:text-white-600 font-semibold text-lg rounded-lg p-4 uppercase">
                <i class="las la-check"></i>
                Uložit
            </button>
        </div>
    </div>

</main>