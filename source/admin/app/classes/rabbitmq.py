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
from mysql.connector import Error


# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.handle_database import Database
from logs import create_log
from random_string import random_string

# IMPORT CONSTANT VARIABLES (/app/variables.py)
from variables import RABBITMQ_URL, RABBITMQ_PORT, RABBITMQ_USERNAME, RABBITMQ_PASSWORD


class RabbitMQ:

    def __init__(self):
        pass
    
    def get_connection(self):
        try:
            credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
            connection = pika.BlockingConnection(pika.ConnectionParameters(RABBITMQ_URL, RABBITMQ_PORT, "/", credentials))

            create_log(type="ALERT", message=f"Connected to RabbitMQ Server")

            return connection
        
        except Exception as e:
            create_log(type="ERROR", message=f"Could not connect to RabbitMQ Server [{ e }]")

  
    def publish_message(self, queue_name=None, message=None):
        try:
            connection = self.get_connection()
            channel = connection.channel()
            channel.queue_declare(queue=queue_name)
            
            channel.basic_publish(
                exchange='', 
                routing_key=queue_name, 
                body=message,
                properties=pika.BasicProperties(delivery_mode=2)
            )

            connection.close()

            create_log(type="ALERT", message=f"Sent message to RabbitMQ Server - queueName: { queue_name }, messsage: { message }")
            return True
        
        except Exception as e:
            create_log(type="ERROR", message=f"Could not send message to RabbitMQ Server - queueName: { queue_name }, messsage: { message } [{ e }]")
            return False
            

    def consume_messages(self, queue_name, callback):
        connection = self.get_connection()
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print(f'[*] Waiting for messages in {queue_name}. To exit press CTRL+C')
        channel.start_consuming()

    def message_callback(self, ch, method, properties, body):
        print(f'Received message: {json.loads(body)["type"]}')