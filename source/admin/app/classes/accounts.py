"""
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

    Jakákoliv úprava a distribuce tohoto kódu 
    bez povolení autora je zakázána!

    © Robin Míček 2023 - 2024

********************************************************
"""

# PACKAGES IMPORTS
import os
import sys

import hashlib

# IMPORTS FROM PACKAGES
from mysql.connector import Error

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.handle_database import Database
from logs import create_log
from random_string import random_string

# IMPORT CONSTANT VARIABLES (/app/variables.py)
from variables import HASH_SALT


class Account:

    def __init__(self):
        pass
    

    def exists(self, email=None):

        db = Database()
        db.connect()

        db.cursor.execute(f"CALL CheckUserExists('{email}', @exists)")
        db.cursor.execute(f"SELECT @exists")
        query = db.cursor.fetchall()
        
        db.close()

        return True if query[0]["@exists"] == 1 else False
        
    
    def user_info(self, email=None):

        db = Database()
        db.connect()

        db.cursor.execute(f"""
            SELECT *
            FROM accounts
            WHERE email = "{email}"
        """)
        query = db.cursor.fetchall()
        
        db.close()

        return query[0] if len(query) != 0 else None
    

    def user_info_from_id(self, accountId=None):

        db = Database()
        db.connect()

        db.cursor.execute(f"""
            SELECT *
            FROM accounts
            WHERE accountId = "{accountId}"
        """)
        query = db.cursor.fetchall()
        
        db.close()

        return query[0] if len(query) != 0 else None
        
    
    def user_info_from_token(self, token=None):

        db = Database()
        db.connect()

        db.cursor.execute(f"""
            SELECT *
            FROM accounts
            WHERE token = "{token}"
        """)
        query = db.cursor.fetchall()
        
        db.close()

        return query[0] if len(query) != 0 else None

    
    def create_new_account(self, email=None, firstname=None,  surname=None, phone=None, password="None", dateOfBirth=None, role=None):

        if self.exists(email=email) == False:
            try:
                db = Database()
                db.connect()
                db.cursor.execute(f"""CALL InsertAccount('{email}', '{phone}','Bearer {self.create_token(string=email)}', '{self.create_hash(string=f"{password[-1]}{HASH_SALT}{password}{email}{password[0]}")}', '{firstname}', '{surname}', '{dateOfBirth}', '{role}')""")
                db.close()

                create_log(type="ALERT", message=f"New user has been created - Email: {email}")

                return True
            
            except Error as e:
                create_log(type="ERROR", message=f"Could not create new user - Email: {email} [{e}]")

                return False

        else:
            return 0


    def auth_password(self, email="None", password="None"):

        db = Database()
        db.connect()

        db.cursor.execute(f"""CALL AuthUserPassword('{email}', '{self.create_hash(string=f"{password[-1]}{HASH_SALT}{password}{email}{password[0]}")}', @auth)""")
        db.cursor.execute(f"SELECT @auth")
        query = db.cursor.fetchall()
        
        db.close()

        return True if query[0]["@auth"] == 1 else False
        
    
    def auth_token(self, token=None):

        db = Database()
        db.connect()

        db.cursor.execute(f"CALL AuthUserToken('{token}', @email)")
        db.cursor.execute(f"SELECT @email")
        query = db.cursor.fetchall()
        
        db.close()

        return query[0]["@email"] if query[0]["@email"] != None else False
        

    def update_token(self, email=None):
        try:
            new_token = self.create_token(string=email)

            db = Database()
            db.connect()
            db.cursor.execute(f"""
                UPDATE accounts
                SET token = "Bearer {new_token}"
                WHERE email = "{email}"
            """)
            db.close()

            create_log(type="ALERT", message=f"Account token has been updated - Email: {email}")

            return new_token
        
        except Error as e:
            create_log(type="ERROR", message=f"Could not update account token - Email: {email} [{e}]")
            
            return False


    def create_hash(self, string=None):

         return (hashlib.sha256(f"{string.encode('utf-8', 'ignore').decode('utf-8')}".encode()).hexdigest())
    

    def create_token(self, string=None):

        return (hashlib.sha256(f"{random_string(length=3)}{string}{random_string(length=7)}".encode()).hexdigest())
    

    def all_accounts(self):

        db = Database()
        db.connect()
        db.cursor.execute("""
            SELECT *
            FROM accounts
        """)
        query = db.cursor.fetchall()
        db.close()

        return query
    

    def update_active(self, accountId=None):

        try:
            db = Database()
            db.connect()
            db.cursor.execute(f"""
                CALL ToggleAccountActive('{accountId}')
            """)
            db.close()

            create_log(type="ALERT", message=f"Toggled account active status - accountId: {accountId}")

        except Exception as e:
            create_log(type="ERROR", message=f"Could not toggle account active status [{e}]")



# Create new admin user if the file is called directly
if __name__ == "__main__":
    try:
        account = Account()
        account.create_new_account(
            email=input("Email: "), 
            firstname=input("Jméno: "), 
            surname=input("Příjmení: "),
            phone=input("Telefonní číslo: "),    
            dateOfBirth=input("Datum narození (YYYY-MM-DD): "), 
            password=input("Heslo: "), 
            role="admin" 
        )

        print("[ALERT] New admin user has been created")

    except Exception as e:
        print(f"[ERROR] Could not create new user [{e}]")