# Startup 

# Change folder ownership to the user that will run the service
```bash
sudo chmod -R a+rwx folderName
```

# Remove __pycache__ folders and .pyc files
```bash
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
```

# Replace
C:\Develop\FoodOrderingSystem\source\admin\app\web\blueprints\b_socketio.py 
from __main__ import socketio -> from app import socketio
```bash
sed -i 's/from __main__ import socketio/from app import socketio/g' ./app/web/blueprints/b_socketio.py
```

# Run the aplication

0. Init database
```bash
docker run -d -p 3306:3306 --name KOkenkuDB -e MYSQL_ROOT_PASSWORD=root mysql:latest
```

```sql
CREATE DATABASE kOkenku
```

1. Install requirements: 
```bash
pip3 install -r sources/admin/app/requirements.txt
```
2. Set enviroment variables

3. Init DB: 
```bash
python3 sources/admin/database/handle_database.py
```

4. Create new user with admin privileges: 
```bash
python3 sources/admin/classes/accounts.py
```

5. Run the server using gunicorn (for long-term deployment create a service):
```bash
gunicorn --bind ip-address:port --chdir /sources/admin/app/web app:app
```


python3 -m gunicorn -k gevent -w "<number of workers>" --bind 0.0.0.0:8000 app:app



1. Přepsat main, upravit variables
2. ./install.sh script
3. init databáze
4. vytvořit nového uživatele