<script>
    import { createEventDispatcher  } from "svelte"
    const dispatch = createEventDispatcher()

    let currentPage = "SETTINGS"
    function changePage(changeTo) {
        currentPage = changeTo
        dispatch("pageChange", currentPage)
    }


    // All buttons
    const allButtons = [ 
        // For each needs to set template they render in the App.svelte router
        {
            "name": "POS",
            "icon": "las la-receipt"
        },
        {
            "name": "WALLETREFILL",
            "icon": "las la-wallet"
        },
        {
            "name": "KITCHENHUB",
            "icon": "las la-desktop"
        },
        {
            "name": "SETTINGS",
            "icon": "las la-tools"
        }
    ]
</script>


<main class="h-full">
    <div class="bg-secondary h-full w-full flex justify-center items-center flex-col rounded-lg">
        
        {#each allButtons as { name, icon }}

            <button on:click={() => changePage(name)} class:bg-white={currentPage == name} class:text-white={currentPage != name} class="my-3 w-full p-4 text-3xl">
                <i class={icon}></i>
            </button>
        
        {/each}

    </div>
</main>