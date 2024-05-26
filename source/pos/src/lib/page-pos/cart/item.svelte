<script>
    // Props
    export let name
    export let quantity
    export let price
</script>


<main>
    <div class="flex gap-3 items-center py-1 px-2 my-1 border-t-2 border-gray-200">

        <h1 class="font-semibold text-sm xl:text-lg">{ quantity }x</h1>
    
        <div class="grow">
            <h1 class="font-semibold text-sm xl:text-lg">{ name }</h1>
        </div>

        <p class="font-bold text-sm xl:text-lg">{ (price * quantity).toFixed(2) } Kč</p>
        
    </div>
</main>