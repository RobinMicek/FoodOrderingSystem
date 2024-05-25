/*
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

********************************************************
*/


// IMPORTS
import axios from 'axios'


// Configuration
export async function getConfiguration() {
    let configuration = null

    const configurationResponse = await axios.get(localStorage.getItem("urlServer") + "/files/storage/texts/config.json");
    if (configurationResponse && configurationResponse.status === 200) {
        configuration = configurationResponse.data
    }
    return configuration
}


export async function getAllEstablishments() {
    try {
        const response = await axios.get(localStorage.getItem("urlServer") + `/api/get-all-establishments`, {
            headers: {
                "Authorization": localStorage.getItem("apiToken") 
            }
        });

        if (response && response.status === 200) {
            return response.data.data
        }
        
    } catch (error) {
        console.log(error)
        return false
    }
}


export async function getWallet() {
    try {
        const cardNumber = localStorage.getItem("merchantCardNumber")

        if( cardNumber != undefined || cardNumber != null ) {
            const response = await axios.get(localStorage.getItem("urlServer") + `/api/get-wallet-card?cardNumber=${ cardNumber }`, {
                headers: {
                    "Authorization": localStorage.getItem("apiToken") 
                }
            });
    
            if (response && response.status === 200) {
                return response.data.data
            }

        } else {
            alert("Nebylo zadáno číslo karty!")
            return false
        }
        
    } catch (error) {
        console.log(error)
        alert("Zjišťení zůstatku se nezdařilo!")
        return false
    }
}


export async function getEstablishmentWallet() {
    try {
        const response = await axios.get(localStorage.getItem("urlServer") + `/api/get-wallet`, {
            headers: {
                "Authorization": localStorage.getItem("apiToken") 
            }
        });

        if (response && response.status === 200) {
            return response.data.data
        }
        
    } catch (error) {
        console.log(error)
        return false
    }
}


export async function refillWallet(amount) {
    try {
        const cardNumber = localStorage.getItem("merchantCardNumber")
        const establishmentId = localStorage.getItem("establishmentId")

        if( cardNumber != undefined || cardNumber != null ) {
            const response = await axios.get(localStorage.getItem("urlServer") + `/api/refill-wallet?cardNumber=${ cardNumber }&establishmentId=${ establishmentId }&amount=${ amount }`, {
                headers: {
                    "Authorization": localStorage.getItem("apiToken") 
                }
            });
    
            if (response && response.status === 200) {
                alert("Peněženka byla úspěšně doplněna!")
                return response.data.data
            }

        } else {
            alert("Nebylo zadáno číslo karty!")
            return false
        }
        
    } catch (error) {
        console.log(error)
        alert("Doplnění peněženky se nezdařilo!")
        return false
    }
}


export async function getAllProducts(establishmentId) {
    try {            
        const response = await axios.get(localStorage.getItem("urlServer") + `/api/get-establishment?establishmentId=${ establishmentId }`, {
            headers: {
                "Authorization": localStorage.getItem("apiToken")
            }
        });

        if (response && response.status === 200) {
            const data = response.data.data.menus
            var allProducts = []

            for (var x = 0; x < data.length; x++) {
                const productsInMenu = await getProductsInMenu(data[x].menuId)
                productsInMenu === false ? (new Error(`Error: Nepodařilo se načíst produkty pro Menu s ID ${ data[x].menuId }`), null) : allProducts.push({"name": data[x].name, "menuId": data[x].menuId, products: productsInMenu});

            }
            return allProducts
        }
        
    } catch (error) {
        console.error(error)
    }
}


export async function getProductsInMenu(menuId) {
    try {
        const response = await axios.get(localStorage.getItem("urlServer") + `/api/get-menu?menuId=${ menuId }`, {
            headers: {
                "Authorization": localStorage.getItem("apiToken") 
            }
        });

        if (response && response.status === 200) {
            return response.data.data.products
        }
        
    } catch (error) {
        console.log(error)
        return false
    }
}


export async function completeOrder(products, paymentType) {
    try {  
        let cardNumber = localStorage.getItem("merchantCardNumber") != null ? localStorage.getItem("merchantCardNumber") : localStorage.getItem("establishmentCardNumber")
        let establishmentId = localStorage.getItem("establishmentId")

        const configuration = await getConfiguration()

        var formattedProducts = []
        var maxPreparationTime = null
        for (var x = 0; x < products.length; x++) {
            var {productId, quantity} = products[x]
            formattedProducts.push({"productId": productId, "quantity": quantity})
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
            'Authorization': localStorage.getItem("apiToken")
        }

        const data = {
            "cardNumber": cardNumber,
            "paymentType": paymentType,
            "establishmentId": parseInt(establishmentId),
            "pickupTime": `${pickupTime.getHours()}:${pickupTime.getMinutes()}`,
            "products": formattedProducts
        }
        
        const response = await axios.post(localStorage.getItem("urlServer")  + "/api/create-order-pos",            
            data,
            { headers }
        );

        if (response && response.status === 200) {            
            return response.data.data
        } else {
            console.error(response)
            return false
        }                        
    } catch (error) {
        console.log(error)
        return false
    }
}
