
## Docker
1. Vytvořte image pomocí Dockerfile
docker build -t kitchenhub:tag .

2. Spusťte kontejner
docker run -d -p 8080:8080 --name kitchenHub kitchenhub:tag

3. Jděte na _localhost:8080_ (popřípadně jiný port, který jste specifikovali při spouštění kontejneru)

4. Proveďte _First Time Setup_ (potřebné informace jsou v _Admin Dashboardu_)