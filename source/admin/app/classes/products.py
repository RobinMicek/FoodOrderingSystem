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

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.handle_database import Database
from random_string import random_string
from logs import create_log

# IMPORT CONSTANT VARIABLES (/app/variables.py)


class Product():

    def __init__(self): 
        pass

    
    def create_new_product(self, data):
        try:
            # Save Image        
            if data["image"] != None:
                parent_dir =  os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

                slug = f"{random_string(length=10)}"
                url_image = f"/files/storage/images/products/{slug}.png"

                data["image"].save(os.path.join(parent_dir, f"web{url_image}"))
            else:
                url_image = "/files/storage/images/products/placeholder.png"


            # Create Product
            db = Database()
            db.connect()
            db.cursor.execute(f"""
                CALL InsertProduct('{data["name"]}', '{str(data["description"])}', '{data["price"]}', '{data["preparationTime"]}', '{url_image}', @insertedID);
            """)
            db.cursor.execute("""
                SELECT @insertedID;
            """)
            productId = db.cursor.fetchall()[0]["@insertedID"]
            db.close()

            create_log(type="ALERT", message=f"Created new product - productId: {productId}")

            return productId
        
        except Exception as e:
            create_log(type="ERROR", message=f"Could not create new product [{e}]")


    def update_product(self, data):

        try:
            db = Database()
            db.connect()

            # Save Image        
            if data["image"] != None:
                parent_dir =  os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
                slug = f"{random_string(length=10)}"
                url_image = f"/files/storage/images/products/{slug}.png"
            
                data["image"].save(os.path.join(parent_dir, f"web{url_image}"))

                # Update Product
                db.cursor.execute(f"""
                    CALL UpdateProductWithImage('{data["productId"]}', '{data["name"]}', '{data["description"]}', '{data["price"]}', '{data["preparationTime"]}', '{url_image}')
                """)
            else:
                # Update Product
                db.cursor.execute(f"""
                    CALL UpdateProductWithoutImage('{data["productId"]}', '{data["name"]}', '{data["description"]}', '{data["price"]}', '{data["preparationTime"]}')
                """)

            db.close()

            create_log(type="ALERT", message=f"""Updated product - productId: {data["productId"]}""")

        except Exception as e:
            create_log(type="ERROR", message=f"Could not update product [{e}]")


    def all_products(self):
        
        db = Database()
        db.connect()
        db.cursor.execute("""
            SELECT *
            FROM products
            ORDER BY productId DESC
        """)
        query = db.cursor.fetchall()
        db.close()

        return query
    

    def info(self, productId):

        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT *,
            TIME_FORMAT(preparationTime, '%H:%i:%s') AS preparationTime
            FROM products
            WHERE productId = "{productId}"
        """)
        query = db.cursor.fetchall()
        db.close()

        return query[0] if len(query) != 0 else []
    

    def update_show(self, productId = None):

        try:
            db = Database()
            db.connect()
            db.cursor.execute(f"""
                CALL ToggleProductShow('{productId}')
            """)
            db.close()

            create_log(type="ALERT", message=f"Toggled product visibility - productId: {productId}")

        except Exception as e:
            create_log(type="ERROR", message=f"Could not toggle product visibility [{e}]")


    def number_of_purchases(self, productId = None, timeWindow = "today"): # timeWindow = today, week, month, year, allTime

        timeWindow = str(timeWindow).upper() if timeWindow != "today" else "DATE"

        db = Database()
        db.connect()

        if timeWindow != "ALLTIME":
            db.cursor.execute(f"""
                SELECT 
                    SUM(orders_products.quantity) AS purchases
                FROM
                    orders_products 
                LEFT JOIN 
                    products
                    ON orders_products.productId = products.productId 
                LEFT JOIN
                    orders
                    ON orders_products.orderId = orders.orderId 
                WHERE
                    products.productId = { productId } AND
                    { timeWindow }(orders.createdTime) = { timeWindow }(CURDATE()) AND
                    orders.status != "CANCELED" 
                GROUP BY 
                    products.productId
            """)
            query = db.cursor.fetchall()

        else: 
            db.cursor.execute(f"""
                SELECT 
                    SUM(orders_products.quantity) AS purchases
                FROM
                    orders_products 
                LEFT JOIN 
                    products
                    ON orders_products.productId = products.productId 
                LEFT JOIN
                    orders
                    ON orders_products.orderId = orders.orderId 
                WHERE
                    products.productId = { productId } AND
                    orders.status != "CANCELED" 
                GROUP BY 
                    products.productId
            """)
            query = db.cursor.fetchall()
        
        db.close()

        return query[0]["purchases"] if len(query) != 0 else None



    def revenue(self, productId = None, timeWindow = "today"): # timeWindow = today, week, month, year, allTime

        timeWindow = str(timeWindow).upper() if timeWindow != "today" else "DATE"

        db = Database()
        db.connect()

        if timeWindow != "ALLTIME":
            db.cursor.execute(f"""
                SELECT 
                    ROUND(SUM(orders_products.price * orders_products.quantity), 2) AS revenue
                FROM
                    orders_products 
                LEFT JOIN 
                    products
                    ON orders_products.productId = products.productId 
                LEFT JOIN
                    orders
                    ON orders_products.orderId = orders.orderId 
                WHERE
                    products.productId = { productId } AND
                    { timeWindow }(orders.createdTime) = { timeWindow }(CURDATE()) AND
                    orders.status != "CANCELED" 
                GROUP BY 
                    products.productId
            """)
            query = db.cursor.fetchall()

        else: 
            db.cursor.execute(f"""
                SELECT 
                    ROUND(SUM(orders_products.price * orders_products.quantity), 2) AS revenue
                FROM
                    orders_products 
                LEFT JOIN 
                    products
                    ON orders_products.productId = products.productId 
                LEFT JOIN
                    orders
                    ON orders_products.orderId = orders.orderId 
                WHERE
                    products.productId = { productId } AND
                    orders.status != "CANCELED" 
                GROUP BY 
                    products.productId
            """)
            query = db.cursor.fetchall()
        
        db.close()

        return query[0]["revenue"] if len(query) != 0 else None
