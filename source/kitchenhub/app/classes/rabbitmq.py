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
import hashlib
import pika
import threading

# IMPORTS FROM PACKAGES


# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.handle_database import Database
from classes.orders import Order
from logs import create_log

# IMPORT CONSTANT VARIABLES (/app/variables.py)
from getConfig import getConfig


class RabbitMQ:

    def __init__(self):
        pass
    
    def get_connection(self):
        try:
            config = getConfig()
            credentials = pika.PlainCredentials(config["rabbitmqUsername"], config["rabbitmqPassword"])
            connection = pika.BlockingConnection(pika.ConnectionParameters(config["rabbitmqUrl"], config["rabbitmqPort"], "/", credentials))

            db = Database()
            db.cursor.execute("""
                UPDATE app_configuration
                SET rabbitmqLastConnected = CURRENT_TIMESTAMP
            """)
            db.close()

            return connection
        
        except Exception as e:
            return False

    def consume_messages(self):
        try:
            queue_name = getConfig()["establishmentSlug"]

            connection = self.get_connection()
            channel = connection.channel()
            channel.queue_declare(queue=queue_name)
            channel.basic_consume(queue=queue_name, on_message_callback=self.message_callback, auto_ack=True)

            create_log(type="ALERT", message=f"Connected to RabbitMQ Server")

            channel.start_consuming()

        except Exception as e:
            create_log(type="ERROR", message=f"Could not connect to RabbitMQ Server [{ e }]")


    def message_callback(self, ch, method, properties, body):

        message = json.loads(body.decode("utf-8"))

        if message.get("type", None) == "newOrder":
            Order().store_orders_from_rabbitmq(order=message["data"])
        
        elif message.get("type", None) == "canceledOrder":
            Order().canceled_order_from_rabbitmq(orderId=message["orderId"])
        
        else:
            create_log(type="ERROR", message=f"Received unknown type of message from RabbitMQ [{ message }]")

       
