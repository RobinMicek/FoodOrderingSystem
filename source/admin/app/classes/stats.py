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

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.handle_database import Database

# IMPORT CONSTANT VARIABLES (/app/variables.py)


class Stats():

    def __init__(self): 
        pass

    
    def transform_data(self, input_data):
        transformed_data = {}
        
        for item in input_data:
            for key, value in item.items():
                if key not in transformed_data:
                    transformed_data[key] = []
                transformed_data[key].append(value)
        
        return transformed_data
    

    def stats_sum(self, rangeFrom=None, rangeTo=None):

        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT
                SUM(stats_daily_overall.total_orders) as total_orders,
                SUM(stats_daily_overall.total_canceled_orders) as total_canceled_orders,
                ROUND(SUM(stats_daily_overall.revenue_total), 2) as revenue_total,
                ROUND(SUM(stats_daily_overall.revenue_cash), 2) as revenue_cash,
                ROUND(SUM(stats_daily_overall.revenue_wallet), 2) as revenue_wallet,
                SUM(stats_daily_overall.new_acc_created) as new_acc_created,
                SUM(stats_daily_overall.total_wallet_refills) as total_wallet_refills,
                ROUND(SUM(stats_daily_overall.total_wallet_refills_amount), 2) as total_wallet_refills_amount,
                ROUND(SUM(stats_daily_overall.average_order_price), 2) as average_order_price
            FROM
                stats_daily_overall
            WHERE
                date <= DATE("{ rangeTo }")
                AND date >= DATE("{ rangeFrom }")
            ORDER BY
                date DESC
        """)
        query = db.cursor.fetchall()
        db.close()
        
        return query[0] if len(query) != 0 else []
    
    
    def stats(self, rangeFrom=None, rangeTo=None):

        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT
                stats_daily_overall.date as date,
                stats_daily_overall.total_orders as total_orders,
                stats_daily_overall.total_canceled_orders as total_canceled_orders,
                stats_daily_overall.revenue_total as revenue_total,
                stats_daily_overall.revenue_cash as revenue_cash,
                stats_daily_overall.revenue_wallet as revenue_wallet,
                stats_daily_overall.new_acc_created as new_acc_created,
                stats_daily_overall.total_wallet_refills as total_wallet_refills,
                stats_daily_overall.total_wallet_refills_amount as total_wallet_refills_amount,
                stats_daily_overall.average_order_price as average_order_price
            FROM
                stats_daily_overall
            WHERE
                date <= DATE("{ rangeTo }")
                AND date >= DATE("{ rangeFrom }")
            ORDER BY
                date DESC
        """)
        query = db.cursor.fetchall()
        db.close()
        
        return query
    
    
    def establishment_sum(self, rangeFrom=None, rangeTo=None, establishmentId=None):

        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT 
                SUM(total_orders) as total_orders, 
                SUM(total_canceled_orders) as total_canceled_orders, 
                ROUND(SUM(revenue_total), 2) as revenue_total, 
                ROUND(SUM(revenue_cash), 2) as revenue_cash, 
                ROUND(SUM(revenue_wallet), 2) as revenue_wallet
            FROM 
                stats_daily_establishments
            WHERE
                date <= DATE("{ rangeTo }")
                AND date >= DATE("{ rangeFrom }")
                AND establishmentId = "{ establishmentId }"
            ORDER BY
                date DESC
        """)
        query = db.cursor.fetchall()
        db.close()
        
        return query[0] if len(query) != 0 else []