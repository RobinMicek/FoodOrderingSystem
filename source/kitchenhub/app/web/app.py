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

import socketio

# IMPORTS FROM PACKAGES
from flask import Flask, Blueprint, request, current_app
from flask_cors import CORS
from flask_socketio import SocketIO

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from web.render_extended_template import render_extended_template

# IMPORT CONSTANT VARIABLES (/app/variables.py)
from variables import FLASK_SECRET_KEY


# INICIALIZE FLASK
def create_app():
    app = Flask(
        __name__,
        static_folder="files")
    app.secret_key = FLASK_SECRET_KEY
    CORS(app)
    
    return app

def create_sioServer(app):
    sioServer = SocketIO(app, cors_allowed_origins="*")
    app.extensions["sioServer"] = sioServer
    return sioServer

app = create_app()


# IMPORT BLUEPRINTS
from blueprints.b_homepage import b_homepage
app.register_blueprint(b_homepage)


from blueprints.b_info import b_info
app.register_blueprint(b_info)


from blueprints.b_funcs import b_funcs
app.register_blueprint(b_funcs, url_prefix="/func")


from blueprints.b_screens import b_screens
app.register_blueprint(b_screens, url_prefix="/screens")


from blueprints.b_auth import b_auth
app.register_blueprint(b_auth)


from blueprints.b_fts import b_fts
app.register_blueprint(b_fts)


# 404 ERROR HANDLING
def handle_bad_request(e):
    return render_extended_template("base.html")
app.register_error_handler(404, handle_bad_request)


# IMPORT ERROR HANDLERS
# from blueprints.b_errors import page_not_found
# app.register_error_handler(404, page_not_found)

# SERVER
from blueprints.socketio import start_socketio_server
sioServer = create_sioServer(app)



# RUN THE FLASK TEST SERVER
if __name__ == "__main__":
    start_socketio_server(sioServer)
    sioServer.run(app, port=8080, host="0.0.0.0", debug=False, allow_unsafe_werkzeug=True) # The port needs to stay the 8080, check /app/classes/orders Order.store_orders_from_socket for info

