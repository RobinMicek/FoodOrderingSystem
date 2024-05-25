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

    
    def create_order(self, data = None):
        try:
            # Validate json
            schema = {
                "type": "object",
                "properties": {
                    "accountId": {"type": "integer", "minimum": 1},
                    "cardNumber": {"type": "string", "minimum": 1},
                    "establishmentId": {"type": "integer", "minimum": 1},
                    "pickupTime": {"type": "string", "minimum": 1},
                    "paymentType": {"type": "string", "minimum": 1},
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
                "required": ["establishmentId", "pickupTime", "products", "accountId", "cardNumber", "paymentType"]
            }
            
            validate(data, schema)

            try:
                # Transform time into a timestamp
                current_datetime = datetime.datetime.now()
                time_obj = datetime.datetime.strptime(data["pickupTime"], "%H:%M").time()
                data["pickupTime"] = datetime.datetime.combine(current_datetime.date(), time_obj)

                # Check if the establishment is open
                establishment = Establishment().all_info(establishmentId=data["establishmentId"])

                if establishment and establishment["isOpen"]["isOpen"] and datetime.datetime.strptime(establishment["isOpen"]["closingTime"], "%H:%M").time() > time_obj:
                    db = Database()
                    db.connect()

                    # If paymentType is wallet, check wallet balance and update if sufficient
                    if data["paymentType"] == "WALLET":
                        wallet_info = Account().user_info_from_id(accountId=data["accountId"])
                        wallet_balance = wallet_info["walletBalance"]
                        total_price = sum(Product().info(productId=prod["productId"])["price"] * prod["quantity"] for prod in data["products"])

                        if wallet_balance >= total_price:
                            db.cursor.execute(f"""
                                UPDATE accounts
                                SET walletBalance = {round(wallet_balance - total_price, 0)}
                                WHERE accountId = {data["accountId"]};
                            """)

                        else:
                            raise Exception("Not enough money in wallet!")


                    # Get all available products from menus
                    available_products = [
                        product["productId"]
                        for menu in establishment["menus"]
                        if Menu().info(menuId=menu["menuId"])["show"] == 1
                        for product in Menu().products(menuId=menu["menuId"])
                        if product["show"] == 1
                    ]
                    are_all_products_available = [ordered_product["productId"] in available_products for ordered_product in data["products"]][0]


                    if are_all_products_available == True:
                        # Create new order
                        db.cursor.execute(f"""
                            CALL InsertOrder('{data["accountId"]}', '{data["establishmentId"]}', '{data["paymentType"] if data["paymentType"] == "WALLET" else "CASH"}', '{data["pickupTime"]}', @insertedID);
                        """)
                        db.cursor.execute("SELECT @insertedID;")
                        order_id = db.cursor.fetchone()["@insertedID"]

                    else:
                        raise Exception("Not all product are available")


                    # Insert products into the order
                    for product in data["products"]:
                        product_info = Product().info(productId=product["productId"])

                        db.cursor.execute(f"""
                            CALL InsertOrderProduct('{order_id}', '{product_info["productId"]}', '{product["quantity"]}', '{product_info["price"]}');
                        """)


                    db.close()

                    create_log(type="ALERT", message=f"Created new order - orderId: {order_id}, establishmentId: {data['establishmentId']}, accountId: {data['accountId']}, cardNumber: {data['cardNumber']}")

                    # Send order information to KitchenHub through socket
                    order_tag = self.send_through_socket(orderId=order_id)
                   
                    return {"orderId": order_id, "tag": order_tag}
                
                else:
                    raise Exception(f"Establishment is closed!")
            
            
            except Exception as e:
                create_log(type="ERROR", message=f"Could not create new order - establishmentId: {data['establishmentId']}, accountId: {data['accountId']}, cardNumber: {data['cardNumber']} [{e}]")
                return False
        

        except Exception as e:
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


            db.cursor.execute(f"""
                CALL CancelOrder('{orderId}');
            """)
            
            # Return money to wallet
            order_info = self.info(orderId=orderId)
            if order_info["paymentType"] == "WALLET":
                Account().refund_money(accountId=order_info["accountId"], amount=order_info["totalPrice"], orderId=orderId)

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
                          
            WHERE 
                orders.establishmentId = "{establishmentId}"
                AND orders.status != "DONE"
                AND orders.status != "CANCELED"

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


            return query["tag"] # Sent as a response to the createOrder request                             

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
