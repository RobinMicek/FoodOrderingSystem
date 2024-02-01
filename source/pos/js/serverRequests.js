class serverRequests {
    
    constructor() {}


    async getAllProducts() {
        try {            
            const response = await axios.get(serverUrl + `/api/get-establishment?establishmentId=${ establishmentId }`, {
                headers: {
                    "Authorization": apiToken
                }
            });

            if (response && response.status === 200) {
                const data = response.data.data.menus
                var allProducts = []

                for (var x = 0; x < data.length; x++) {
                    const productsInMenu = await this.getProductsInMenu(data[x].menuId)
                    productsInMenu === false ? (new Error(`Error: Nepodařilo se načíst produkty pro Menu s ID ${ data[x].menuId }`), null) : allProducts = allProducts.concat(productsInMenu);

                }
                return allProducts
            }
            
        } catch (error) {
            console.error(error)
        }
    }


    async getProductsInMenu(menuId) {
        try {
            const response = await axios.get(serverUrl + `/api/get-menu?menuId=${ menuId }`, {
                headers: {
                    "Authorization": apiToken 
                }
            });

            if (response && response.status === 200) {
                return response.data.data.products
            }
            
        } catch (error) {
            consolele.log(error)
            return false
        }
    }


    async completeOrder(products) {
        try {        
            const configuration = await getConfiguration(

            )
            var formattedProducts = []
            var maxPreparationTime = null
            for (var x = 0; x < products.length; x++) {
                var {productId, qty} = products[x]
                formattedProducts.push({"productId": productId, "quantity": qty})
                
                if (products[x].preparationTime !== undefined && (maxPreparationTime === null || products[x].preparationTime > maxPreparationTime)) {
                    maxPreparationTime = products[x].preparationTime
                }    
            }


            if (configuration.orders.ignorePreparationTimes) {
                maxPreparationTime = configuration.orders.defaultOrderWait

                const pad = (maxPreparationTime) => String(maxPreparationTime).padStart(2, '0')
                const defaultWaitHours = pad(Math.floor(maxPreparationTime / 3600))
                const defaultWaitMinutes = pad(Math.floor((maxPreparationTime % 3600) / 60))
                const defaultWaitSeconds = 0 // pad(maxPreparationTime % 60)

                maxPreparationTime = `${defaultWaitHours}:${defaultWaitMinutes}:${defaultWaitSeconds}`
            }

            const currentTime = new Date()
            const [prepHours, prepMinutes, prepSeconds] = maxPreparationTime.split(":").map(Number)
            const pickupTime = new Date(currentTime.getFullYear(), currentTime.getMonth(), currentTime.getDate(), 
                currentTime.getHours() + prepHours, currentTime.getMinutes() + prepMinutes + 1, currentTime.getSeconds() + prepSeconds)


            const headers = {
                'Content-Type': 'application/json',
                'Authorization': apiToken
            }

            const data = {
                "establishmentId": establishmentId,
                "pickupTime": `${pickupTime.getHours()}:${pickupTime.getMinutes()}`,
                "products": formattedProducts
            }
            
            const response = await axios.post(serverUrl + "/api/create-order",            
                data,
                { headers }
            );

            if (response && response.status === 200) {            
                return response.data.data
            } else {
                alert(response)
                return false
            }                        
        } catch (error) {
            console.log(error)
            return false
            
        }
    }
}