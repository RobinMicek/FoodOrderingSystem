<script>
    // Import components
    import Product from "./products/product.svelte";
    import Menu from "./products/menu.svelte"


    // Load menu on init
    let menus = JSON.parse(localStorage.getItem("menus"))

    // Change menu
    let selectedMenuId = 999
    function handleChangeMenu (event) {
        selectedMenuId = event.detail
    }
        
</script>


<main class="h-full w-full flex flex-col">
    
    <div class="px-4 flex overflow-auto gap-4">
        {#each menus as { name, menuId }}
            <Menu on:changeMenu={ handleChangeMenu } name={ name } menuId={ menuId } selected={ true ? selectedMenuId == menuId : false }/>
        {/each}
    </div>

    <hr class="w-11/12 text-center m-auto my-4">

    <!-- Products -->
    <div class="px-4 overflow-y-scroll h-32 flex-grow">
        {#if menus[menus.findIndex(item => item.menuId == selectedMenuId)]  != undefined }
            <div class="grid grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4 ">
                {#each menus[menus.findIndex(item => item.menuId == selectedMenuId)].products as { name, price, imagePath, productId, preparationTime }}
                    <Product name={ name } price={ price } productId={ productId } imagePath={ imagePath } preparationTime={ preparationTime } />
                {/each}
            </div>
            {:else }
            <div class="text-center col-span-3 xl:col-span-4 2xl:col-span-5 h-full flex justify-center items-center flex-col text-white space-y-5">
                <i class="las la-hand-pointer text-8xl"></i>
                <h1 class="text-2xl">Pro zobrazení produktů zvolte menu na horní liště</h1>
            </div>
        {/if}
    </div>
</main>