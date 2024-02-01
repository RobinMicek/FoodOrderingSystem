# Jak spustit K Okénku | Backend & Admin Panel 

## Docker
Nejjednodušší cestou jak spustit __K Okénku Admin__ je jako kontejner pomocí Dockeru.

Tento způsob rovnou spouští i kontejner s MySQL databází. Pokud jí nechcete, je potřeba z _./Compose.yml_ souboru odstranit _mysql_ service a _depends-on_ u _kokenku-admin_ service.

1. Je potřeba mít nainstalovaný __Docker__ a __Docker Compose__
    ```bash
    curl -fsSL https://get.docker.com -o get-docker.sh
    ``` 
    
    ```bash
    sh get-docker.sh
    ``` 

2. Upravte __Environment Variables__ v _./Compose.yml_
    - Nastavte:
        - __MYSQL_ROOT_PASSWORD__ - Musí být stejné jako  __KO_DB_PASSWORD__
        -  __KO_HASH_SALT__ - Náhodný řetezec, který se přidává do hashovaní hesel uživatel 

3. Spušťte kontejnery
    ```bash
    docker compose up -d
    ```

4. Připojte se k terminálu "kokenku-admin" kontejneru
    - Zjistěte ID kontejneru
        ```bash
        docker ps
        ```

    - Připojte se k terminálu
        ```bash
        docker exec -it <id-kontejneru> bash
        ```

5. Inicializujte databázi
    ```bash
    python3 ./app/database/handle_database.py
    ```

6. Vytvořte administrátorský účet
    ```bash
    python3 ./app/classes/accounts.py
    ```

7. Admin Web UI by nyní mělo být přístupné na _localhost:8000_



## Manuálně

1. Nahradťe __ __main__ __ za app v ./app/web/blueprints/b_socketio.py 
    ```bash
    sed -i 's/from __main__ import socketio/from app import socketio/g' ./app/web/blueprints/b_socketio.py
    ```

2. Vytvořte datábazi na vašem MySQL serveru
    ```sql
    CREATE DATABASE kOkenku
    ```

3. Uložte přihlašovací údaje k MySQL databázi jako _environment variables_
    ```bash
    export \
        KO_DB_HOST= \
        KO_DB_NAME=kOkenku \
        KO_DB_USER= \
        KO_DB_PASSWORD= \
        KO_HASH_SALT= \
    ```

4. Nainstalujte Python a potřebné knihovky
    ```bash
    sudo apt update && sudo apt upgrade
    ```

    ```bash 
    sudo apt install python3 python3-pip
    ```

    ```bash
    pip3 install -r ./app/requirements.txt
    ```

5. Inicializujte databázi 
    ```bash
    python3 ./app/database/handle_database.py
    ```

6. Vytvořte administrátorský účet
    ```bash
    python3 ./app/classes/accounts.py
    ```

7. Přidejte Systemd service
    -
7. Admin Web UI by nyní mělo být přístupné na _localhost:8000_   

