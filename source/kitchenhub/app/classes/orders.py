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
import json
import datetime
import requests

# IMPORTS FROM PACKAGES

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.handle_database import Database
from classes.server_requests import ServerRequests

from flask import current_app

from logs import create_log

# IMPORT CONSTANT VARIABLES (/app/variables.py)


class Order():

    def __init__(self): 
        pass


    def all_local_orders(self):
        db = Database()
        orders = db.fetch_as_json(f"""
            SELECT *
            FROM ORDERS
            ORDER BY orders.orderId DESC
        """)

        for order in orders:
            order["products"] = db.fetch_as_json(f"""
            SELECT orders_products.*
            FROM orders
            
            LEFT JOIN orders_products
            ON orders.orderId = orders_products.orderId
                                            
            WHERE orders.orderId = '{order["orderId"]}'                                               
        """)
            
        db.close()

        return orders


    def store_orders_from_api(self):
        # This function stores all orders for the establishment
        # that it gets from the BackEnd server.
        # But before it may delete  locally stored orders and their progress,
        # so use with caution!!!

        try:
            all_orders = ServerRequests().get_all_orders()

            if all_orders != False:
                db = Database()

                for order in all_orders:

                    # Compare local status with the api response
                    synced = db.fetch_as_json(f"""
                        SELECT synced
                        FROM orders
                        WHERE orderId = '{order["orderId"]}'
                    """)

                    if len(synced) == 0 or synced[0]["synced"] == None or synced[0]["synced"] == 1 or order["status"] == "CANCELED":
                    
                        # Delete local order
                        db.cursor.execute(f"""
                            DELETE FROM orders
                            WHERE orderId = '{order["orderId"]}'
                        """)
                        db.cursor.execute(f"""
                            DELETE FROM orders_products
                            WHERE orderId = '{order["orderId"]}'
                        """)


                        db.cursor.execute(f"""
                            INSERT INTO orders
                                (orderId, firstname, surname, email, phone, totalPrice, establishmentId, tag, pickupTime, status, synced)
                            VALUES
                                ('{order["orderId"]}', '{order["firstname"]}', '{order["surname"]}', '{order["email"]}', '{order["phone"]}', '{order["totalPrice"]}', '{order["establishmentId"]}', '{order["tag"]}', '{order["pickupTime"]}', '{order["status"]}', 1)
                        """)

                        for product in order["products"]:
                            db.cursor.execute(f"""
                                INSERT INTO orders_products
                                    (orderId, name, orderPrice, preparationTime, quantity)
                                VALUES
                                    ('{order["orderId"]}', '{product["name"]}', '{product["price"]}', '{product["preparationTime"]}', '{product["quantity"]}')
                            """)

                db.cursor.execute("""
                    UPDATE app_configuration
                    SET lastSync = CURRENT_TIMESTAMP
                """)
                
                db.close()

                # Send all orders through local socket 
                self.send_orders_local_socket()

                create_log(type="ALERT", message=f"Got orders from BackEnd server")

        except Exception as e:
                create_log(type="ERROR", message=f"Could not get orders from BackEnd server [{e}]")


    def store_orders_from_rabbitmq(self, order = None):
        # This function stores new order received by RabbitMQ.

        try:            
            if order != None:
                db = Database()

                # Compare local status with the api response
                synced = db.fetch_as_json(f"""
                    SELECT synced
                    FROM orders
                    WHERE orderId = '{order["orderId"]}'
                """)

                if len(synced) == 0 or synced[0]["synced"] == None or synced[0]["synced"] == 1 or order["status"] == "CANCELED":
                
                    # Delete local order
                    db.cursor.execute(f"""
                        DELETE FROM orders
                        WHERE orderId = '{order["orderId"]}'
                    """)
                    db.cursor.execute(f"""
                        DELETE FROM orders_products
                        WHERE orderId = '{order["orderId"]}'
                    """)


                    db.cursor.execute(f"""
                        INSERT INTO orders
                            (orderId, firstname, surname, email, phone, totalPrice, establishmentId, tag, pickupTime, status, synced)
                        VALUES
                            ('{order["orderId"]}', '{order["firstname"]}', '{order["surname"]}', '{order["email"]}', '{order["phone"]}', '{order["totalPrice"]}', '{order["establishmentId"]}', '{order["tag"]}', '{order["pickupTime"]}', '{order["status"]}', 1)
                    """)

                    for product in order["products"]:
                        db.cursor.execute(f"""
                            INSERT INTO orders_products
                                (orderId, name, orderPrice, preparationTime, quantity)
                            VALUES
                                ('{order["orderId"]}', '{product["name"]}', '{product["price"]}', '{product["preparationTime"]}', '{product["quantity"]}')
                        """)
                
                db.close()

                # Send all orders through local socket 
                # Im sending through http request because the socketio needs flask aplication context
                # so it needs an active request to be able to send messages from the server
                sendOrders = requests.get("http://localhost:8080/func/send-local-socket")

                create_log(type="ALERT", message=f"Got new order from RabbitMQ [orderId: {order['orderId']}]")

        except Exception as e:
                create_log(type="ERROR", message=f"Could not store order from RabbitMQ [{e}]")


    def canceled_order_from_rabbitmq(self, orderId = None):
        # This function updates status to canceled for a order received by RabbitMQ.

        try:            
            if orderId != None:
                db = Database()                
                db.cursor.execute(f"""
                    UPDATE orders
                    SET status = 'CANCELED'
                    WHERE orderId = '{orderId}'
                """)
                db.close()

                # Send all orders through local socket 
                # Im sending through http request because the socketio needs flask aplication context
                # so it needs an active request to be able to send messages from the server
                sendOrders = requests.get("http://localhost:8080/func/send-local-socket")

                create_log(type="ALERT", message=f"Canceled an order from RabbitMQ [orderId: {orderId}]")

        except Exception as e:
                create_log(type="ERROR", message=f"Could not cancel an order from RabbitMQ [{e}]")


    def sync_local_orders(self):
        # This function synchronizes local orders with the BackEnd server.

        try:
            db = Database()
            orders = db.fetch_as_json(f"""
                SELECT 
                    orderId, status
                FROM orders                
                WHERE synced = 0
            """)

            for order in orders:
                response = ServerRequests().update_order_status(orderId=order["orderId"], newStatus=order["status"])

                if response == True:
                    db.cursor.execute(f"""
                        UPDATE orders
                        SET synced = 1
                        WHERE orderId = '{order["orderId"]}'
                    """)

                    create_log(type="ALERT", message=f"Synced order status [orderId: {order['orderId']}, syncedStatus: {order['status']}]")
                
            db.close()

        except Exception as e:
            create_log(type="ERROR", message=f"Could not sync orders status with the BackEnd server [{e}]")
    

    def toggle_local_status(self, orderId = None):          
        try:
            db = Database()
            current_status = db.fetch_as_json(f"""
                SELECT status
                FROM orders
                WHERE orderId = '{orderId}'
            """)[0]["status"]

            statuses = ["CREATED", "PROCESSING", "READY", "DONE"]
            next_status = statuses[statuses.index(current_status) + 1] if statuses[statuses.index(current_status)] != "DONE" else "DONE"
            
            db.cursor.execute(f"""
                UPDATE orders
                SET
                    status = "{next_status}",
                    synced = 0
                WHERE orderId = '{orderId}'
            """)                
            db.close()

            # Send all orders through local socket 
            self.send_orders_local_socket()


            # Sync with backend
            self.sync_local_orders()

            create_log(type="ALERT", message=f"Toggled local order status to '{next_status}' [orderId: {orderId}]")
            return True

        except Exception as e:
            create_log(type="ERROR", message=f"Could not update local status [orderId: {orderId}] [{e}]")
            return False
        

    def send_orders_local_socket(self):
        # This method requires a valid flask request
        try:
            
            orders = self.all_local_orders()

            from flask import current_app
            socketio = current_app.extensions['socketio']
         
            socketio.emit('allOrders', {
                "msg": "All local orders.",
                "data": json.dumps(orders)
            })

            create_log(type="ALERT", message=f"Sent orders through local socket")

        except Exception as e:
            create_log(type="ERROR", message=f"Could not send orders through local socket [{e}]")
