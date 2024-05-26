<script>
    let urlKitchenHub = localStorage.getItem("urlKitchenHub")
    let kitchenHubShowPage = localStorage.getItem("kitchenHubShowPage")
</script>


<main class="h-full w-full">
    <div class="px-4 w-full h-full">
        <iframe src={ urlKitchenHub + "/screens/" + kitchenHubShowPage } title="KitchenHub" frameborder="0" class="w-full h-full rounded-lg"></iframe>
    </div>
</main>