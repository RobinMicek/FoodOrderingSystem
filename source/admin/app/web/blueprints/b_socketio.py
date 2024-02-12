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

# IMPORTS FROM PACKAGES
from flask import Flask, Blueprint, render_template, request, redirect, jsonify
from flask_socketio import SocketIO, emit, disconnect, join_room

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.establishments import Establishment

# IMPORT CONSTANT VARIABLES (/app/variables.py)


# INICIALIZE SOCKETIO
from __main__ import socketio

# EVENTS 
@socketio.on('connect')
def socketio_handle_connection():

    # Auth
    slug = request.args.get("slug", None)
    token = request.args.get("token", None)
    establishmentId = Establishment().auth(slug=slug, token=token)

    if establishmentId != False:
        join_room(slug)

        emit("authCompleted", {
            "authStatus": True,
            "establishmentId": establishmentId
        }, room=slug)
    
    else: 
        emit("authCompleted", {
            "authStatus": False
        })

        # Disconnect the user
        disconnect(request.sid, namespace='/')



# Send message from the server without any previous interaction by the client
# 
# from flask import current_app
# socketio = current_app.extensions['socketio']
# socketio.emit('', {})
