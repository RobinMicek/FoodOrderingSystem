<script>
    // IMPORTS
    import { createEventDispatcher  } from "svelte"
    const dispatch = createEventDispatcher()

    export let name
    export let menuId
    export let selected
</script>

<main>
    <button on:click={ () => dispatch("changeMenu", menuId) } class:bg-secondary={selected == true} class="border-2 border-secondary hover:bg-secondary rounded-lg overflow-hidden relative shadow-lg h-16 w-auto p-4">
        <h1 class="font-semibold text-white text-xl text-nowrap">{ name }</h1>
    </button>
</main>