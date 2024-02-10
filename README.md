# O projektu
Systém pro objednávání a vyvolávání objednávek pro fast food, který zjednoduší a zrychlí proces objednávání a výdeje jídla. Systém se skládá ze 4 komponent, které vzájemně spolupracují, aby zajistily maximální pohodlí a efektivitu:

1. BackEnd Server a Admin Dashboard:
BackEnd Server je srdcem celého systému. Zpracovává objednávky, komunikuje s ostatními komponentami a uchovává veškerá data. Admin Dashboard umožňuje manažerovi sledovat stav objednávek v reálném čase, konfigurovat systém a analyzovat statistiky.


2. KitchenHub - Vyvolávací obrazovky:
Systém, který běží na jednotlivých provozovnách. Obsluha přes něj přijímá objednávky a jejich stav se synchronizuje na ostatních obrazovkých. Zákazníci tak snadno vidí, kdy si mohou vyzvednout své hotové jídlo.


3. Mobilní aplikace:
Pomocí mobilní aplikace si zákazníci pohodlně prohlédnou menu, vytvoří a odešlou objednávku a můžou sledovat její stav.


4. POS (Point of Sale):
Pokladní systém slouží obsluze k přijímání objednávek a plateb od zákazníků. Systém je integrován s BackEnd Serverem, takže se objednávky automaticky přenáší do kuchyně a eliminuje se tak manuální zadávání.

Tento text zpracovala umělá inteligence


## Jak to celé funguje dohromady
![image](/sketches/App%20Diagram.jpg)


# Instalace
- Návod pro zprovoznění daných komponent je popsán v _README.md_ souboru v root složce zdrojového kódu dané komponenty (_./source/komponenta/README.md_)
- Všechny komponenty (kromě mobilní aplikace) jsou spustitelné pomocí Dockeru, včetně všech ostatních potřebných programů (MySQL,...)
- Pro build mobilní aplikace je zapotřebí Android Studio/XCode
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