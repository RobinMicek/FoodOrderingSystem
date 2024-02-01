# Předpřipravené prostředí
V rámci usnadnění rozběhnutí tohoto projektu jsou předpřipravené některé komponenty a jejich hosting.
- BackEnd server je dostupný na adrese _http://robinmicek.cz_
- _APK_ mobilní aplikace je dostupné v root složce zdrojového kódu


## Demo přihlašovací údaje
Admin uživatel:
- Email: 
- Heslo: 

API token pro POS je dostupný v Admin Dashboardu.


# O projektu
Projekt obsahuje 4 komponenty
1. BackEnd Server + Admin Dashboard
2. KitchenHub
3. Mobilní aplikace
4. POS

## Jak to celé funguje dohromady
![image](/sketches/App%20Diagram.jpg)


# Instalace
- Návod pro zprovoznění daných komponent je popsán v _README.md_ souboru v root složce zdrojového kódu dané komponenty (_./source/komponenta/README.md_)
- Všechny komponenty (kromě mobilní aplikace) jsou spustitelné pomocí Dockeru, včetně všech ostatních potřebných programů (MySQL,...)
- Pro vlastí build mobilní aplikace je zapotřebí Android Studio/XCode - V root složce je dostupné hotové _APK_, pro instalaci na zařízení s OS Android
- Pro připojení mobilní aplikace k REST Api serveru je zapotřebí, aby server měl SSL certifikát, jinak requesty neprojdou - Problém je někde v kombinaci VueJS, CapacitorJS a Androidu


# Assety třetích stran

## Textové editory
- https://alex-d.github.io/Trumbowyg/
- https://github.com/josdejong/jsoneditor


## Ikony
- https://icons8.com/line-awesome
- https://feathericons.com/

## Fonty
- https://fonts.google.com/specimen/M+PLUS+Rounded+1c?previewtext=gh%C4%8D%C5%A1s%2B%C4%9B%C5%A1%C4%8D%C5%99%C5%BE%C3%BD%C3%A1%C3%AD%C3%A9&preview.text_type=custom

## Obrázky
- https://www.pexels.com/cs-cz/foto/drevo-restaurace-lide-zena-2788792/

## Grafy
- https://www.chartjs.org/

## Softwarové komponenty/knihovny třetích stran
- FrontEnd POSu vychází z https://github.com/emsifa/tailwind-pos
- https://tailwindcss.com/
- https://capacitorjs.com/
- https://github.com/fengyuanchen/vue-qrcode


# Working time
start: 10.06.2023
end: 


# Notes
local notifications / not push 