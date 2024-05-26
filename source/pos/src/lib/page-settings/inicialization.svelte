<script>
    // IMPORTS
    import { getAllEstablishments, getEstablishmentWallet, getConfiguration, getAllProducts } from "../../utils/serverRequests"


    let allEstablishments
    async function getEstablishments () {
        allEstablishments = await getAllEstablishments()
    }

    let ftsComplete
    async function selectEstablishment (establishmentId, establishmentName) {
        try{
            let configuration = await getConfiguration()
            localStorage.setItem("establishmentId", establishmentId)
            localStorage.setItem("establishmentName", establishmentName)
            localStorage.setItem("establishmentCardNumber", (await getEstablishmentWallet()).cardNumber)
            localStorage.setItem("companyName", configuration.companyInfo.companyName)
            localStorage.setItem("companyAddress", configuration.companyInfo.address)
            localStorage.setItem("companyPhone",configuration.companyInfo.phone)
            localStorage.setItem("companyCIN", configuration.companyInfo.CIN)

            localStorage.setItem("menus", JSON.stringify(await getAllProducts(establishmentId=establishmentId)))

            ftsComplete = true

            alert("Inicializace proběhla úspěšně!")
        }
        catch(error) {
            console.error(error)
            alert("Inicializace se nezdařila!")
        }
        
    }


</script>

<main class="h-full w-full">

    <div class="h-full w-full p-4 flex flex-col">
        {#if allEstablishments && !ftsComplete }
            <div class="flex-grow h-32 overflow-y-scroll space-y-4rounded-lg p-4 space-y-4">
                <h1 class="text-center text-2xl text-white font-semibold uppercase">Zvolte provozovnu</h1>        
                {#each allEstablishments as { name, establishmentId, address }}
                    <button on:click={ async () => selectEstablishment(establishmentId, name)} class="hover:bg-secondary border-2 border-secondary text-white p-4 w-full rounded-lg">
                        <h1 class="text-lg font-semibold">{ name }</h1>
                        <p>{ address }</p>
                    </button>
                {/each}
            </div>
        {:else if ftsComplete}
            <div>

            </div>
        {:else} 
            <button on:click={ async () => getEstablishments()} class="font-semibold text-white border-2 p-4 w-full border-secondary hover:bg-transparent bg-secondary text-lg uppercase rounded-lg"> 
                <i class="las la-redo-alt"></i> 
                Provést inicializaci 
            </button>
        {/if}
    </div>

</main>