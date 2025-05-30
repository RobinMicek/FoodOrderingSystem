/*
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

********************************************************
*/


// This file stores all the necesary
// variables for this app to function.

import axios from 'axios'


export const serverUrl = "" // Url Address of the Admin Server - Must be HTTPS && without '/'

export const appName = "K Okénku"


// Configuration
export async function getConfiguration() {
  let configuration = null

  const configurationResponse = await axios.get(serverUrl + "/files/storage/texts/config.json");
  if (configurationResponse && configurationResponse.status === 200) {
    configuration = configurationResponse.data
  }
  
  return configuration
}