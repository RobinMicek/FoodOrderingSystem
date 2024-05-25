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
import { writable } from "svelte/store";


export const cart = writable([])

export const isMerchantCartSubmited = writable(true ? localStorage.getItem("merchantCardNumber") != null : false)