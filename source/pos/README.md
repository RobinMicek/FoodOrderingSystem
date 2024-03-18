# O pokladní systému
Tato komponenta vznikla jako demostrace API, jakožto ukázka toho, že ji lze využít i pro jiné účely, než jen zákaznickou mobilní aplikaci. 

FrontEnd a základní funkce vychází z projektu https://github.com/emsifa/tailwind-pos

# Jak spustit
1. Je potřeba vytvořit _api_ účet

2. Následně jděte do _./src/js/variables.js a vyplntě potřebné proměnné
    - serverUrl = URL adresa serveru (adresa admin dashboardu)
    - apiToken = Token vytvořeného _api_ účtu (k dostání v admin dashboardu)

3. Nainstalujte potřebné knihovny
    ```bash
    npm install
    ```

4. Vytvořte nový build (Musíte provést jako administrátor)
    ```bash
    npm run package
    ```

5. Ve složce _./builds_ naleznete instalátor