# Jak spustit
1. Vytvořte image pomocí Dockerfile
    ```bash
    docker build -t kitchenhub .
    ```

2. Spusťte kontejner
    ```bash
    docker run -d -p 8080:8080 --name kitchenHub kitchenhub
    ```

3. Jděte na _localhost:8080_ (popřípadně jiný port, který jste specifikovali při spouštění kontejneru)

4. Proveďte _First Time Setup_ (potřebné informace jsou v _Admin Dashboardu_)