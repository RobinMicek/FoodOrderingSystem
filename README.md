# O projektu
Systém pro objednávání a vyvolávání objednávek pro fast food, který zjednoduší a zrychlí proces objednávání a výdeje jídla. Systém se skládá ze 4 komponent, které vzájemně spolupracují, aby zajistily maximální pohodlí a efektivitu:

1. BackEnd Server a Admin Dashboard:
BackEnd Server je srdcem celého systému. Zpracovává objednávky, komunikuje s ostatními komponentami a uchovává veškerá data. Admin Dashboard umožňuje manažerovi sledovat stav objednávek v reálném čase, konfigurovat systém a analyzovat statistiky.

    ![image](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
    ![image](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
    ![image](https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white)
    ![image](https://img.shields.io/badge/Socket.io-black?style=for-the-badge&logo=socket.io&badgeColor=010101)



2. KitchenHub - Vyvolávací obrazovky:
Systém, který běží na jednotlivých provozovnách. Obsluha přes něj přijímá objednávky a jejich stav se synchronizuje na ostatních obrazovkých. Zákazníci tak snadno vidí, kdy si mohou vyzvednout své hotové jídlo.

    ![image](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
    ![image](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
    ![image](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
    ![image](https://img.shields.io/badge/Socket.io-black?style=for-the-badge&logo=socket.io&badgeColor=010101)



3. Mobilní aplikace:
Pomocí mobilní aplikace si zákazníci pohodlně prohlédnou menu, vytvoří a odešlou objednávku a můžou sledovat její stav.
    
    ![image](https://img.shields.io/badge/Capacitor-119EFF?style=for-the-badge&logo=Capacitor&logoColor=white)
    ![image](https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D)
    ![image](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
    
    ![image](https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white)
    ![image](https://img.shields.io/badge/iOS-000000?style=for-the-badge&logo=ios&logoColor=white)


4. POS (Point of Sale):
Pokladní systém slouží obsluze k přijímání objednávek a plateb od zákazníků. Systém je integrován s BackEnd Serverem, takže se objednávky automaticky přenáší do kuchyně a eliminuje se tak manuální zadávání.
    
    ![image](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
    ![image](https://img.shields.io/badge/alpinejs-white.svg?style=for-the-badge&logo=alpinedotjs&logoColor=%238BC0D0)
    ![images](https://img.shields.io/badge/Electron-191970?style=for-the-badge&logo=Electron&logoColor=white)


## Jak to celé funguje dohromady
![image](/sketches/App%20Diagram.jpg)


# Instalace
- Návod pro zprovoznění daných komponent je popsán v _README.md_ souboru v root složce zdrojového kódu dané komponenty (_./source/komponenta/README.md_)
- Pro build mobilní aplikace je zapotřebí Android Studio/XCode
- Pro připojení mobilní aplikace k REST Api serveru je zapotřebí, aby server měl SSL certifikát, jinak requesty neprojdou - Problém je někde v kombinaci VueJS, CapacitorJS a Androidu


# Assety třetích stran

## Textové editory
- https://alex-d.github.io/Trumbowyg/
- https://github.com/josdejong/jsoneditor


## Ikony
- https://icons8.com/line-awesome
- https://feathericons.com/
- https://flowbite.com/icons/

## Fonty
- https://fonts.google.com/specimen/M+PLUS+Rounded+1c?previewtext=gh%C4%8D%C5%A1s%2B%C4%9B%C5%A1%C4%8D%C5%99%C5%BE%C3%BD%C3%A1%C3%AD%C3%A9&preview.text_type=custom

## Obrázky
- https://www.pexels.com/cs-cz/foto/drevo-restaurace-lide-zena-2788792
- https://www.pexels.com/cs-cz/foto/jidlo-talir-zdravy-restaurace-1352262
- https://www.pexels.com/cs-cz/foto/jidlo-salat-zdravy-menu-4551971
- https://www.pexels.com/cs-cz/foto/1307698


## Grafy
- https://www.chartjs.org/

## Softwarové komponenty/knihovny třetích stran
- FrontEnd POSu vychází z https://github.com/emsifa/tailwind-pos
- https://tailwindcss.com/
- https://capacitorjs.com/
- https://github.com/fengyuanchen/vue-qrcode
