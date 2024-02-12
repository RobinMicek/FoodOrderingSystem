# O pokladní systému
Tato komponenta vznikla jako demostrace API, jakožto ukázka toho, že ji lze využít i pro jiné účely, než jen zákaznickou mobilní aplikaci. 

FrontEnd a základní funkce vychází z projektu https://github.com/emsifa/tailwind-pos

# Jak spustit
1. Je potřeba vytvořit _api_ účet

2. Následně jděte do _./js/variables.js a vyplntě potřebné proměnné
    - serverUrl = URL adresa serveru (adresa admin dashboardu)
    - apiToken = Token vytvořeného _api_ účtu (k dostání v admin dashboardu)

3. Vytvořte image pomocí Dockerfile
    ```bash
    docker build -t kokenku-pos .
    ```

4. Spusťte kontejner
    ```bash
    docker run -d -p 5000:80 --name KOkenkuPOS kokenku-pos
    ```

5. Jděte na _localhost_ (popřípadně s jiným portem, který jste specifikovali při spouštění kontejneru)
