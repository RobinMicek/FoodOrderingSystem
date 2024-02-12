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

import datetime

# IMPORTS FROM PACKAGES
import json

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.handle_database import Database

# IMPORT CONSTANT VARIABLES (/app/variables.py)


class Info():

    def __init__(self) -> None:
        
        pass

    
    def orders(self):
        db = Database()
        orders = db.fetch_as_json("""
            SELECT 
                COUNT(orderId) as totalOrders,
                SUM(CASE WHEN status = 'CREATED' THEN 1 ELSE 0 END) AS created,
                SUM(CASE WHEN status = 'PROCESSING' THEN 1 ELSE 0 END) AS processing,
                SUM(CASE WHEN status = 'READY' THEN 1 ELSE 0 END) AS ready,
                SUM(CASE WHEN status = 'DONE' THEN 1 ELSE 0 END) AS done,
                SUM(CASE WHEN status = 'CANCELED' THEN 1 ELSE 0 END) AS canceled,
                SUM(CASE WHEN synced = '0' THEN 1 ELSE 0 END) AS notSynced
            FROM orders
        """)[0]
        db.close()

        return orders



    