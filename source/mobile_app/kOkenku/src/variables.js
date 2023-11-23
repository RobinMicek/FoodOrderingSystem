// This file stores all the necesary
// variables for this app to function.

import axios from 'axios'


export const serverUrl = "https://robinmicek.tech" // Must be HTTPS && without '/'

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