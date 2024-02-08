// This file stores all the necesary
// variables for this app to function.


// Configuration
async function getConfiguration() {
    let configuration = null
  
    const configurationResponse = await axios.get(serverUrl + "/files/storage/texts/config.json");
    if (configurationResponse && configurationResponse.status === 200) {
      configuration = configurationResponse.data
    }
    return configuration
}


const serverUrl = ""
const apiToken = ""
const establishmentId = 0 // Replace with actual Establishment ID 

const companyName = ""
const establishmentName = ""

const receiptPrefix = ""
