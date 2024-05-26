<script>
    // Import components
    import Inicialization from "./page-settings/inicialization.svelte"
    import VariablesConfig from "./page-settings/variablesConfig.svelte";
</script>

<main class="w-full h-full grid grid-cols-2 gap-4 px-10">
    
    <div class="col-span-1 space-y-4">
        <VariablesConfig /> 
    </div> 
    
    <div class="col-span-1 text-center h-full">
        <Inicialization />
    </div>
    
</main>