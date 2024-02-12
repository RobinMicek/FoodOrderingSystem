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
    

    def stats(self):

        db = Database()
        db.connect()

        data = {
            "orders": {
                "max": {
                    "today": 0,
                    "month": 0,
                    "year": 0,
                    "allTime": 0
                },
                "count": {
                    "today": 0,
                    "month": 0,
                    "year": 0,
                    "allTime": 0
                }
            },
            "revenue": {
                    "today": 0,
                    "month": 0,
                    "year": 0,
                    "allTime": 0
                }
            }

        # TimeWindow
        for timeWindow in ["DATE", "MONTH", "YEAR"]:
            db.cursor.execute(f"""
                SELECT ROUND(MAX(totalPrice), 2) AS totalPrice
                FROM (
                    SELECT SUM(orders_products.quantity * orders_products.price) AS totalPrice
                    FROM orders_products
                    LEFT JOIN orders ON orders.orderId = orders_products.orderId
                    WHERE 
                        { timeWindow }(orders.createdTime) = { timeWindow }(CURRENT_DATE())
                        AND orders.status != "CANCELED"
                    GROUP BY orders.orderId
                ) AS subquery
            """)
            maxOrder = db.cursor.fetchall()[0]

            db.cursor.execute(f"""
                SELECT 
                    COUNT(orders.orderId) AS orders
                FROM
                    orders 
                LEFT JOIN 
                    establishments
                    ON establishments.establishmentId = orders.establishmentId 
                WHERE                     
                    { timeWindow }(orders.createdTime) = { timeWindow }(CURDATE())  
                    AND orders.status != "CANCELED"
            """)
            countOrders = db.cursor.fetchall()[0]


            db.cursor.execute(f"""
                SELECT ROUND(MAX(totalRevenue), 2) AS totalRevenue
                FROM (
                    SELECT SUM(orders_products.quantity * orders_products.price) AS totalRevenue
                    FROM orders_products
                    LEFT JOIN orders ON orders.orderId = orders_products.orderId
                    WHERE 
                        { timeWindow }(orders.createdTime) = { timeWindow }(CURRENT_DATE())
                        AND orders.status != "CANCELED"
                ) AS subquery
            """)
            revenue = db.cursor.fetchall()[0]

            timeWindow = timeWindow.lower() if timeWindow != "DATE" else "today"
            data["orders"]["max"][timeWindow] = maxOrder
            data["orders"]["count"][timeWindow] = countOrders
            data["revenue"][timeWindow] = revenue


        # All Time
        db.cursor.execute(f"""
            SELECT ROUND(MAX(totalPrice), 2) AS totalPrice
            FROM (
                SELECT SUM(orders_products.quantity * orders_products.price) AS totalPrice
                FROM orders_products
                LEFT JOIN orders ON orders.orderId = orders_products.orderId
                WHERE orders.status != "CANCELED"
                GROUP BY orders.orderId
            ) AS subquery
        """)
        maxOrder = db.cursor.fetchall()[0]

        db.cursor.execute(f"""
            SELECT 
                COUNT(orders.orderId) AS orders
            FROM
                orders 
            LEFT JOIN 
                establishments
                ON establishments.establishmentId = orders.establishmentId 
            WHERE
                orders.status != "CANCELED"
        """)
        countOrders = db.cursor.fetchall()[0]


        db.cursor.execute(f"""
            SELECT ROUND(MAX(totalRevenue), 2) AS totalRevenue
            FROM (
                SELECT SUM(orders_products.quantity * orders_products.price) AS totalRevenue
                FROM orders_products
                LEFT JOIN orders ON orders.orderId = orders_products.orderId
                WHERE orders.status != "CANCELED"
            ) AS subquery
        """)
        revenue = db.cursor.fetchall()[0]

        data["orders"]["max"]["allTime"] = maxOrder
        data["orders"]["count"]["allTime"] = countOrders
        data["revenue"]["allTime"] = revenue


        db.close()

        return data
    

    def most_purchased_products(self, timeWindow="today"): # timeWindow options: today, week, month, year

        timeWindow = str(timeWindow).upper() if timeWindow != "today" else "DATE"

        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT
                products.productId,
                products.name,
                products.price,
                SUM(orders_products.quantity) AS totalPurchased
            FROM
                products
            LEFT JOIN
                orders_products ON products.productId = orders_products.productId
            JOIN
                orders ON orders_products.orderId = orders.orderId
            WHERE
                { timeWindow }(orders.createdTime) = { timeWindow }(CURDATE())
                AND orders.status != "CANCELED"
            GROUP BY
                products.productId
            ORDER BY
                totalPurchased DESC
            LIMIT
                10
        """)
        query = db.cursor.fetchall()
        db.close()

        return self.transform_data(query)
    

    def most_visited_establishments(self, timeWindow="today"): # timeWindow options: today, week, month, year

        timeWindow = str(timeWindow).upper() if timeWindow != "today" else "DATE"

        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT
                SUM(orders.establishmentId) AS totalOrders,
                establishments.establishmentId,
                establishments.name
            FROM
                orders
            LEFT JOIN
                establishments ON orders.establishmentId = establishments.establishmentId
            WHERE
                { timeWindow }(orders.createdTime) = { timeWindow }(CURDATE())
                AND orders.status != "CANCELED"
            GROUP BY
                establishments.establishmentId
            ORDER BY
                totalOrders DESC
            LIMIT
                10                    
        """)
        query = db.cursor.fetchall()
        db.close()

        return self.transform_data(query)
        

    def revenue_per_day(self):

        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT
                DATE_FORMAT(DATE(orders.createdTime), '%d. %m. %y') AS orderDate,
                DATE_FORMAT(DATE(orders.createdTime), '%Y-%m-%d') AS sortableDate,
                SUM(products.price * orders_products.quantity) AS totalRevenue
            FROM
                orders
            JOIN
                orders_products ON orders.orderId = orders_products.orderId
            JOIN
                products ON orders_products.productId = products.productId
            WHERE
                orders.status != "CANCELED"
            GROUP BY
                orderDate, sortableDate
            ORDER BY
                sortableDate ASC
        """)
        query = db.cursor.fetchall()
        db.close()

        return self.transform_data(query)
        
    
    def revenue_per_hour(self):

        db = Database()
        db.connect()
        db.cursor.execute(f"""
           SELECT
                DATE_FORMAT(DATE_ADD(CURDATE(), INTERVAL hour HOUR), '%H') AS orderHour,
                COALESCE(SUM(products.price * orders_products.quantity), 0) AS totalRevenue,
                COALESCE(COUNT(DISTINCT orders.orderId), 0) AS totalOrders
            FROM (
                SELECT 0 AS hour UNION ALL
                SELECT 1 UNION ALL
                SELECT 2 UNION ALL
                SELECT 3 UNION ALL
                SELECT 4 UNION ALL
                SELECT 5 UNION ALL
                SELECT 6 UNION ALL
                SELECT 7 UNION ALL
                SELECT 8 UNION ALL
                SELECT 9 UNION ALL
                SELECT 10 UNION ALL
                SELECT 11 UNION ALL
                SELECT 12 UNION ALL
                SELECT 13 UNION ALL
                SELECT 14 UNION ALL
                SELECT 15 UNION ALL
                SELECT 16 UNION ALL
                SELECT 17 UNION ALL
                SELECT 18 UNION ALL
                SELECT 19 UNION ALL
                SELECT 20 UNION ALL
                SELECT 21 UNION ALL
                SELECT 22 UNION ALL
                SELECT 23
            ) AS Hours
            LEFT JOIN
                orders ON DATE(orders.createdTime) = CURDATE() AND HOUR(orders.createdTime) = Hours.hour
            LEFT JOIN
                orders_products ON orders.orderId = orders_products.orderId
            LEFT JOIN
                products ON orders_products.productId = products.productId
            GROUP BY
                orderHour
            ORDER BY
                orderHour
        """)
        query = db.cursor.fetchall()
        db.close()

        return self.transform_data(query)
    

    def revenue_per_establishment(self, timeWindow="today"): # timeWindow options: today, week, month, year

        timeWindow = str(timeWindow).upper() if timeWindow != "today" else "DATE"

        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT
                establishments.name,
                COUNT(orders.orderId) AS totalOrders,
                COALESCE(SUM(orders_products.price * orders_products.quantity), 0) AS totalRevenue
            FROM
                establishments
            LEFT JOIN
                orders ON establishments.establishmentId = orders.establishmentId
            LEFT JOIN
                orders_products ON orders.orderId = orders_products.orderId
            WHERE
                { timeWindow }(orders.createdTime) = { timeWindow }(CURDATE()) 
                AND orders.status != "CANCELED"
            GROUP BY
                establishments.name
            ORDER BY
                totalRevenue DESC
        """)
        query = db.cursor.fetchall()
        db.close()

        return self.transform_data(query)