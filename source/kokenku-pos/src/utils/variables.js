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





export const serverUrl = localStorage.getItem("urlServer") // Url Address of the Admin Server - Must be HTTPS && without '/' (e.g. https://example.com)
export const apiToken = localStorage.getItem("apiToken")