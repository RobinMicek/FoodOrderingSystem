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

import datetime

# IMPORTS FROM PACKAGES
import json
from jsonschema import validate

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.products import Product
from classes.establishments import Establishment
from classes.menus import Menu
from classes.accounts import Account

from database.handle_database import Database
from random_string import random_string, random_string_without_numbers
from logs import create_log

from flask import current_app

# IMPORT CONSTANT VARIABLES (/app/variables.py)


class Order():

    def __init__(self): 
        pass

    
    def create_order(self, data):
        try:
            # Validate json
            schema = {
                "type": "object",
                "properties": {
                    "accountId": {"type": "integer", "minimum": 1},
                    "establishmentId": {"type": "integer", "minimum": 1},
                    "pickupTime": {"type": "string"},
                    "products": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "productId": {"type": "integer", "minimum": 1},
                                "quantity": {"type": "integer", "minimum": 1}
                            },
                            "required": ["productId", "quantity"]
                        }
                    }
                },
                "required": ["establishmentId", "pickupTime", "products", "accountId"]
            }

            
            validate(data, schema)

            try:
                # Transform time into a timestamp
                current_datetime = datetime.datetime.now()
                time_obj = datetime.datetime.strptime(data["pickupTime"], "%H:%M").time()
                data["pickupTime"] = datetime.datetime.combine(current_datetime.date(), time_obj)

                # Check if the establishment is open
                establishment = Establishment().all_info(establishmentId=data["establishmentId"])
                
                if establishment != [] and establishment["isOpen"]["isOpen"] == True and datetime.datetime.strptime(establishment["isOpen"]["closingTime"], "%H:%M").time() > time_obj:

                    # Create new order
                    db = Database()
                    db.connect()
                    db.cursor.execute(f"""
                        CALL InsertOrder('{data["accountId"]}', '{data["establishmentId"]}', '{random_string_without_numbers(length=4)}', '{data["pickupTime"]}', @insertedID);
                    """)
                    db.cursor.execute("""
                        SELECT @insertedID;
                    """)
                    orderId = db.cursor.fetchall()[0]["@insertedID"]


                    # Get all available products from menus
                    available_products = []
                    for menu in establishment["menus"]:
                        for product in Menu().products(menuId=menu["menuId"]):
                            if product["show"] == 1:
                                available_products += [product["productId"]]

                    # Insert Products
                    for product in data["products"]:                        
                        product_info = Product().info(productId=product["productId"])

                        if product != [] and product_info["productId"] in available_products:
                            db.cursor.execute(f"""
                                CALL InsertOrderProduct('{orderId}', '{product_info["productId"]}', '{product["quantity"]}', '{product_info["price"]}')                  
                            """)

                        else:
                            db.close()
                            create_log(type="ERROR", message=f"""Could not create new order - unable to order a product - productId: {data["productId"]}""")
                            return False


                    db.close()
                
                    create_log(type="ALERT", message=f"Created new order - orderId: {orderId}")                    

                    # Send information about the order to KitchenHub through socket
                    self.send_through_socket(orderId=orderId)

                    return orderId
                
                else:
                    create_log(type="ERROR", message=f"""Could not create order - establishment is closed - establishmentId: {data["establishmentId"]}, accountId: {data["accountId"]}""")
                    return False
            
            except Exception as e:
                create_log(type="ERROR", message=f"Could not create new order [{e}]")
                return False


        except json.JSONDecodeError:
            create_log(type="ERROR", message=f"Could not create new order - Request JSON did not match the schema [{data}] [{e}]")
            return False


    def info(self, orderId = None):

        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT
            orders.*,
            accounts.firstname,
            accounts.surname,
            accounts.email,
            accounts.phone,
            establishments.name,
            ROUND(SUM(orders_products.quantity * orders_products.price), 2) AS totalPrice

            FROM orders

            LEFT JOIN accounts
            ON orders.accountId = accounts.accountId

            LEFT JOIN orders_products
            ON orders.orderId = orders_products.orderId 
            
            LEFT JOIN establishments
            ON orders.establishmentId = establishments.establishmentId

            WHERE orders.orderId = "{orderId}"
            GROUP BY orders.orderId
        """)
        query = db.cursor.fetchall()
        db.close()

        return query[0] if len(query) != 0 else []
    

    def products(self, orderId = None):
        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT 
            orders_products.quantity,
            orders_products.price as orderPrice,
            products.*,
            TIME_FORMAT(products.preparationTime, '%H:%i:%s') AS preparationTime

            FROM orders_products

            LEFT JOIN products
            ON  orders_products.productId = products.productId 

            WHERE orders_products.orderId = "{orderId}"
        """)
        query = db.cursor.fetchall()
        db.close()

        return query
    

    def toggle_status(self, orderId = None):

        db = Database()
        db.connect()
        db.cursor.execute(f"""
            CALL ToggleOrderStatus('{orderId}');
        """)
        db.close()

    
    def cancel_order(self, orderId = None):

        try:
            db = Database()
            db.connect()
            db.cursor.execute(f"""
                CALL CancelOrder('{orderId}');
            """)

            # Get establishment slug
            db.cursor.execute(f"""
                SELECT
                    establishments.slug
                    
                FROM orders

                LEFT JOIN establishments
                ON orders.establishmentId = establishments.establishmentId 

                WHERE orderId = '{orderId}'
            """)
            slug = db.cursor.fetchall()[0]["slug"]
            db.close()


            # Send message to the socket about the new order
            socketio = current_app.extensions['socketio']
            socketio.emit('canceledOrder', {
                    "msg": "Order has been canceled.",
                    "orderId": orderId
                },
                room=slug
            )

            create_log(type="ALERT", message=f"Sent info about canceled order through socketio - orderId: {orderId}")   
                            
        except Exception as e:
            create_log(type="ERROR", message=f"Could not send info about canceled order through socket - orderId: {orderId} [{e}]")                    


    def all_orders(self):
        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT
            orders.*,
            accounts.firstname,
            accounts.surname,
            accounts.email,
            establishments.name,
            ROUND(SUM(orders_products.quantity * orders_products.price), 2) AS totalPrice

            FROM orders

            LEFT JOIN accounts
            ON orders.accountId = accounts.accountId

            LEFT JOIN orders_products
            ON orders.orderId = orders_products.orderId 
            
            LEFT JOIN establishments
            ON orders.establishmentId = establishments.establishmentId

            GROUP BY orders.orderId
            ORDER BY orders.orderId DESC
        """)
        query = db.cursor.fetchall()
        db.close()

        return query
    
    
    def all_account_orders(self, accountId = None):
        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT
            orders.*,
            establishments.name,
            ROUND(SUM(orders_products.quantity * orders_products.price), 2) AS totalPrice
            
            FROM orders

            LEFT JOIN orders_products 
            ON orders.orderId = orders_products.orderId 

            LEFT JOIN establishments 
            ON orders.establishmentId = establishments.establishmentId

            WHERE orders.accountId = "{accountId}"

            GROUP BY orders.orderId
            ORDER BY orders.orderId DESC
        """)
        query = db.cursor.fetchall()
        db.close()

        return query
    

    def all_establishment_orders_kitchenhub(self, establishmentId):
        # Only use this function for the KitchenHub API 
        # - Packages all information into one response, 
        # including product names etc.

        db = Database()
        db.connect()
        db.cursor.execute(f"""
            SELECT
                orders.*,
                accounts.firstname,
                accounts.surname,
                accounts.email,
                accounts.phone,
                ROUND(SUM(orders_products.quantity * orders_products.price), 2) AS totalPrice

            FROM orders

            LEFT JOIN accounts
            ON orders.accountId = accounts.accountId

            LEFT JOIN orders_products
            ON orders.orderId = orders_products.orderId 

            LEFT JOIN establishments
            ON orders.establishmentId = establishments.establishmentId
                          
            WHERE orders.establishmentId = "{establishmentId}"

            GROUP BY 
                orders.orderId,
                accounts.firstname,
                accounts.surname,
                accounts.email

            ORDER BY orders.orderId DESC
        """)
        query = db.cursor.fetchall()
        db.close()
        
        # Get products
        for order in query:
            order["products"] = self.products(orderId=order["orderId"])
            order["pickupTime"] = order["pickupTime"].isoformat()    
            del order["createdTime"]
            del order["lastUpdate"]    

        return query
    

    def send_through_socket(self, orderId = None):
        # Only use this function for the KitchenHub Socket
        # - Packages all information into one response, 
        # including product names etc.

        try:
            db = Database()
            db.connect()
            db.cursor.execute(f"""
                SELECT
                    orders.*,
                    accounts.firstname,
                    accounts.surname,
                    accounts.email,
                    accounts.phone,
                    establishments.slug,
                    ROUND(SUM(orders_products.quantity * orders_products.price), 2) AS totalPrice

                FROM orders

                LEFT JOIN accounts
                ON orders.accountId = accounts.accountId

                LEFT JOIN orders_products
                ON orders.orderId = orders_products.orderId
                            
                LEFT JOIN establishments
                ON orders.establishmentId = establishments.establishmentId
                            
                WHERE orders.orderId = "{orderId}"

                GROUP BY 
                    orders.orderId,
                    accounts.firstname,
                    accounts.surname,
                    accounts.email
            """)
            query = db.cursor.fetchall()[0]
            

            query["products"] = self.products(orderId=orderId)

            query["pickupTime"] = query["pickupTime"].isoformat()        
            del query["createdTime"]
            del query["lastUpdate"]

            
            # Send message to the socket about the new order
            socketio = current_app.extensions['socketio']
            socketio.emit('newOrder', {
                    "msg": "New order has been created.",
                    "data": json.dumps(query)
                },
                room=query["slug"]
            )


            # If sent, update it in the database
            db.cursor.execute(f"""
                CALL SocketSentOrder('{orderId}')
            """)

            db.close()

            create_log(type="ALERT", message=f"Sent new order through socketio - orderId: {orderId}")   

                             

        except Exception as e:
            create_log(type="ERROR", message=f"Could not send new order through socket - orderId: {orderId} [{e}]")                    
    

    def update_status(self, orderId = None, newStatus = None):

        try:
            db = Database()
            db.connect()
            db.cursor.execute(f"""
                CALL UpdateOrderStatus('{orderId}', '{newStatus}');
            """)
            db.close()

            create_log(type="ALERT", message=f"Updated order status [orderId: {orderId}, newStatus: {newStatus}]")

        except Exception as e:
            create_log(type="ERROR", message=f"Could not update order's status [orderId: {orderId}, newStatus: {newStatus}] [{e}]")
