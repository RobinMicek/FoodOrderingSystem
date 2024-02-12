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

import socketio

# IMPORTS FROM PACKAGES
from flask import request, Blueprint
from flask_socketio import SocketIO, emit, disconnect, join_room

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from logs import create_log
from database.handle_database import Database
from flask import current_app

from classes.orders import Order

# IMPORT CONSTANT VARIABLES (/app/variables.py)
from getConfig import getConfig


# EVENTS 
# CLIENT - Communication with the backend server
sioClient = socketio.Client()


def socketioClient_connect():
    CONFIG = getConfig()

    if not sioClient.connected:
        sioClient.connect(f"{CONFIG['serverUrl']}?slug={CONFIG['establishmentSlug']}&token={CONFIG['establishmentToken']}")


def socketioClient_reconnect():
    CONFIG = getConfig()

    if sioClient.connected:
        sioClient.disconnect()

    sioClient.connect(f"{CONFIG['serverUrl']}?slug={CONFIG['establishmentSlug']}&token={CONFIG['establishmentToken']}")


@sioClient.on('connect')
def socketioClient_onConnect():
    db = Database()
    db.cursor.execute("""
        UPDATE app_configuration
        SET socketClientConnected = 1
    """)
    db.close()

    create_log(type="ALERT", message=f"Connected to the socketio server [BackEnd Connection]")


@sioClient.on('newOrder')
def socketioClient_newOrder(data):
    Order().store_orders_from_socket(order=json.loads(data["data"]))


@sioClient.on('canceledOrder')
def socketioClient_newOrder(data):
    Order().canceled_order_from_socket(orderId=data["orderId"])
    

@sioClient.on('disconnect')
def socketioClient_disconnect():
    db = Database()
    db.cursor.execute("""
        UPDATE app_configuration
        SET socketClientConnected = 0
    """)
    db.close()

    create_log(type="ERROR", message=f"Disconnected from the socketio server [BackEnd Connection]")
    


# SERVER - Communication with the frontend screens

# Initialize and run the Socket.IO server
def start_socketio_server(sioServer):

    @sioServer.on('connect', namespace='/')
    def socketioServer_handle_connection():
        pin = request.args.get("pin", None)
        CONFIG = getConfig()

        if CONFIG != None: # Configuration is created in the first time setup
            if int(pin) == int(CONFIG["pin"]):
                emit("authCompleted", {
                    "authStatus": True
                })

                create_log(type="ALERT", message=f"'{request.sid}' connected to the local socketio server [Local Connection]")

                # Send all local orders
                Order().send_orders_local_socket()
            
            else: 
                emit("authCompleted", {
                    "authStatus": False

                })

                # Disconnect the user
                disconnect(request.sid, namespace='/')
                create_log(type="ERROR", message=f"'{request.sid}' could not connect to the local socketio server [Local Connection]")

        else:
            # Disconnect the user
            disconnect(request.sid, namespace='/')
            create_log(type="ERROR", message=f"Missing configuration [Local Connection]")



    @sioServer.on('disconnect', namespace='/')
    def socketioServer_handle_connection():
        create_log(type="ALERT", message=f"'{request.sid}' disconnected from the local socketio server [Local Connection]")
