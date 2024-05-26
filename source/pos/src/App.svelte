<script>
  // Navbar
  import Navbar from "./lib/navbar.svelte"

  let currentPage = "SETTINGS"
  function handlePageChange(event) {
    currentPage = event.detail
  }


  // Import pages
  import POS from "./lib/page-pos.svelte"
  import WalletRefills from "./lib/page-walletRefills.svelte"
  import KitchenHub from "./lib/page-kitchenhub.svelte"
  import Settings from "./lib/page-settings.svelte"
</script>

<main class="no-print">
  <div class="h-screen w-screen p-5 bg-primary">
    <div class="h-full w-full grid grid-cols-20">

      <div class="col-span-1 h-full w-full">
        <Navbar on:pageChange={handlePageChange}/>
      </div>

      <div class="col-span-19 h-full w-full">
        {#if currentPage === "POS"}
          <POS/>
        <!--{:else if currentPage === "TABLES"}
        tables-->
        {:else if currentPage === "WALLETREFILL"}
          <WalletRefills/>
        {:else if currentPage === "KITCHENHUB"}
          <KitchenHub/>
        {:else if currentPage === "SETTINGS"}
          <Settings/>
        {/if}
      </div>

    </div>
  </div>
</main>
