/*
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

********************************************************
*/


// This function check the demanded products are able to be prepared within
// the time the establishment has until it closes.

import { getObject, removeObject } from "@/utils/storage.js"
import { CartObject } from "@/utils/cart.js"

import { serverUrl, getConfiguration } from "@/variables.js"

import axios from 'axios'
import { add, sub, format } from 'date-fns'


export async function checkForPickupTimeWindow (establishmentId) {

    try {
        // Get establishment opening hours
        const token = await getObject("token")
        
        const response = await axios.get(serverUrl + "/api/get-establishment?establishmentId=" + establishmentId, {
            headers: {
            "Authorization": token 
            }
        })

        if (response && response.status === 200) {
            const establishmentOpeningHours = response.data.data.isOpen
            const cartObject = new CartObject(establishmentId)
            const fullCart = await cartObject.getCart()
            const products = fullCart.products

            const configuration = await getConfiguration()

            if (establishmentOpeningHours && establishmentOpeningHours.isOpen == true && products && products.length != 0) {
                if (configuration.orders.ignorePreparationTimes === false) {

                    // Find the highest product preparation time                    
                    var maxPreparationTime = null
                
                    products.forEach(product => {
                        const preparationTime = product.preparationTime
                    
                        // Check if pickupTime is defined and greater than the current highest
                        if (preparationTime !== undefined && (maxPreparationTime === null || preparationTime > maxPreparationTime)) {
                            maxPreparationTime = preparationTime
                        }
                    })

                }
                else {
                    var maxPreparationTime = configuration.orders.defaultOrderWait

                    const pad = (num) => String(num).padStart(2, '0')
                    const defaultWaitHours = pad(Math.floor(maxPreparationTime / 3600))
                    const defaultWaitMinutes = pad(Math.floor((maxPreparationTime % 3600) / 60))
                    const defaultWaitSeconds = 0 // pad(maxPreparationTime % 60)

                    maxPreparationTime = `${defaultWaitHours}:${defaultWaitMinutes}:${defaultWaitSeconds}`
                }
                    
                
                // Get the time window
                const currentTime = new Date()

                const [closeHours, closeMinutes] = establishmentOpeningHours.closingTime.split(':').map(Number)
                const closingTime = new Date()
                closingTime.setHours(closeHours, closeMinutes, "00")

                const [prepHours, prepMinutes, prepSeconds] = maxPreparationTime.split(":").map(Number)
                const earliestPickupTime = add(currentTime, { hours: prepHours, minutes: prepMinutes, seconds: prepSeconds })
                const latestPickupTime = sub(closingTime, { hours: prepHours, minutes: prepMinutes, seconds: prepSeconds })


                if (earliestPickupTime.getTime() < closingTime.getTime()) {
                    return {
                        "closingTime": format(closingTime, 'HH:mm'),
                        "preparationTime": maxPreparationTime,
                        "earliestPickupTime": format(earliestPickupTime, 'HH:mm'),
                        "latestPickupTime": format(latestPickupTime, 'HH:mm')
                    }
                } else {
                    return false
                }
                
            } else {
                return false
            }
        } else {
            return false
        }

    } catch (error) {
        await removeObject("token")
        return false
    } 
}