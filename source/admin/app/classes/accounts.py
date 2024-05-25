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
        
    
    def user_info_from_email(self, email=None):

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
        
    
    def user_info_from_cardnumber(self, card_number=None):

        db = Database()
        db.connect()

        db.cursor.execute(f"""
            SELECT *
            FROM accounts
            WHERE cardNumber = "{card_number}"
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

                create_log(type="ALERT", message=f"New account has been created - Email: {email}")

                return True
            
            except Error as e:
                create_log(type="ERROR", message=f"Could not create new account - Email: {email} [{e}]")

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
            ORDER BY accounts.accountId DESC
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


    def refill_wallet(self, accountId=None, amount=None, establishmentId=None):

        try:
            db = Database()
            db.connect()
            db.cursor.execute(f"""
                CALL RefillWalletBalance('{accountId}', '{amount}', '{establishmentId}')
            """)
            db.close()

            create_log(type="ALERT", message=f"Refilled wallet - accountId: {accountId}, amount: {amount}")

            return True

        except Exception as e:
            create_log(type="ERROR", message=f"Could not refill wallet - accountId: {accountId}, amount: {amount} [{e}]")
            return False
    
    
    def refund_money(self, accountId=None, amount=None, orderId=None):

        try:
            db = Database()
            db.connect()
            db.cursor.execute(f"""
                CALL RefundMoneyFromCanceledOrder('{accountId}', '{amount}')
            """)
            db.close()

            create_log(type="ALERT", message=f"Refunded money from canceled order - orderId: {orderId}, accountId: {accountId}, amount: {amount}")

            return True

        except Exception as e:
            create_log(type="ERROR", message=f"Could not refund money from canceled order - orderId: {orderId}, accountId: {accountId}, amount: {amount} [{e}]")
            return False

    def get_all_account_refills(self, accountId=None):
        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT 
                accounts_wallet_refills.refillId,
                accounts_wallet_refills.amount, 
                accounts_wallet_refills.date,
                establishments.establishmentId,
                establishments.name 
            FROM
                accounts_wallet_refills
            LEFT JOIN
                accounts
            ON
                accounts.accountId = accounts_wallet_refills.accountId 
            LEFT JOIN
                establishments
            ON
                establishments.establishmentId = accounts_wallet_refills.establishmentId 
            WHERE
                accounts.accountId = {accountId}
            ORDER BY
                accounts_wallet_refills.date DESC
        """)
        query = db.cursor.fetchall()
        db.close()

        return query




# Create new account if the file is called directly
if __name__ == "__main__":
    try:
        accountTypes = ["admin", "user", "pos"]
        accountType = input(f"Typ účtu | Možnosti: {', '.join(accountTypes)} (U POS účtů se v Admin Dashboardu zobrazuje API Token): ")
        while accountType not in accountTypes: accountType = input(f"Zadejte správný typ účtu ({', '.join(accountTypes)}): ")

        account = Account()
        if accountType == "pos":
            account.create_new_account(
                email=input("Emailová adresa (společně s heslem slouží k získání tokenu, nemusí být reálná): "), 
                firstname=input("Název účtu: "), 
                surname="",
                phone="",    
                dateOfBirth="1989-03-12", 
                password=input("Heslo: "), 
                role="pos" 
            )
        else:
            account.create_new_account(
                email=input("Emailová adresa: "), 
                firstname=input("Jméno: "), 
                surname=input("Příjmení: "),
                phone=input("Telefonní číslo: "),    
                dateOfBirth=input("Datum Narození (YYYY-MM-DD): "), 
                password=input("Heslo: "), 
                role=accountType 
            )

        print("[ALERT] New user has been created")

    except Exception as e:
        print(f"[ERROR] Could not create new user [{e}]")