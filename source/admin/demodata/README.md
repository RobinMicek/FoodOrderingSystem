# Co jsou to demodata?
Demodata jsou předpřivanené produkty, menu a provozovny. Využívají se pro účely vývoje a demonstrace.

-  Obsahují: 
    - 18 Produktů
    - 6 Menu
    - 1 Provozovna
    - Základní Konfigurace


# Jak přidat demodata

1. Zkopírujte složku ___./storage___ do ___/app/web/files___ (nahraďte s ní aktuální složku ___storage___)

2. Ve vaší MySQL databázi proveďte skript ___demodata.sql___

### Poznámka
Demodata je nutná inicializovat v čisté databázi (po provedeni skriptu ___/app/database/handle_database.py__), jinak by se mohlo stát, že by neseděli ID.


