"""
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

********************************************************
"""

# PACKAGES IMPORTS
import os
import sys

import mysql.connector

# IMPORTS FROM PACKAGES
from mysql.connector import Error

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from logs import create_log


# IMPORT CONSTANT VARIABLES (/app/variables.py)
from variables import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_SSL_CA


class Database():

    def __init__(self):

        self.name = DB_NAME
        self.user = DB_USER 
        self.password = DB_PASSWORD 

        self.host = DB_HOST
        self.ssl_ca = DB_SSL_CA 
    

    def connect(self):

        try: 
            config = {
                "database": self.name, 
                "user": self.user, 
                "password": self.password, 
                "host": self.host, 
                "port": "3306"
            }

            self.db = mysql.connector.connect(**config)
            self.cursor = self.db.cursor(dictionary=True)
        
        except Error as e:
            create_log(type="ERROR", message=f"Could not connect the database [{e}]")


    def close(self):

        self.db.commit()
        self.db.close()    


    def initialize(self):
        # Initializes new database with all the necesary tables etc.
        # SQL script is saved in sql/init.sql and sql/procedures.sql files. 
        self.connect()
        try:
            for x in self.handle_sql_file(filename="init.sql"):
                self.cursor.execute(x)
            for x in self.handle_sql_file(filename="procedures.sql"):
                self.cursor.execute(x)
            for x in self.handle_sql_file(filename="procedures-stats.sql"):
                self.cursor.execute(x)
            for x in self.handle_sql_file(filename="triggers.sql"):
                self.cursor.execute(x)
            for x in self.handle_sql_file(filename="events.sql"):
                self.cursor.execute(x)

            create_log(type="ALERT", message="Database has been inicialized.")
            print("[ALERT] Database has been inicialized.")

        except Error as e:
            create_log(type="ERROR", message=f"Could not inicialize the database [{e}]")
            print(f"[ERROR] Could not inicialize the database [{e}]")

        self.close()


    def clear(self):
        # Clears used database.
        # SQL script is saved in sql/clear.sql file. 
        self.connect()
        try:
            for x in self.handle_sql_file(filename="clear.sql"):                
                self.cursor.execute(x)
            
            create_log(type="ALERT", message="Database has been cleaned.")
            print("[ALERT] Database has been cleaned.")

        except Error as e:
            create_log(type="ERROR", message=f"Could not clear the database [{e}]")
            print(f"[ERROR] Could not clear the DB [{e}]")

        self.close()


    def handle_sql_file(self, filename=None):
        # This function takes a SQL script file and splits it into individual statements. 
        # I'm doing this because I had problems with executing multiple statements 
        # as one using cursor.exetute(x, multi=True)

        # This function only takes files from the /sql/ directory

        with open(os.path.join(os.path.dirname(__file__), "sql/" + str(filename)), "r+") as f:

            script = f.read()

            if filename == "init.sql" or filename == "events.sql" or filename == "clear.sql":
                script = script.split(";")
                for x in script:
                    x.replace(";", "")

            elif filename == "procedures.sql" or filename == "procedures-stats.sql" or filename == "triggers.sql":
                script = script.split("//")
                for x in script:
                    x.replace("//", "")

        return script
    

# Inicialize the DB if the file is called directly
if __name__ == "__main__":
    confirmation = input("Opravdu chcete zinicializovat databázi - může mít za následek ztrátu dat (y/n)? ").lower()
    while confirmation not in ["y", "n"]:
        confirmation = input("Prosím zadejte 'y' pro ano nebo 'n' pro ne: ").lower()

    if confirmation == "y":
        db = Database()
        db.clear()
        db.initialize()
