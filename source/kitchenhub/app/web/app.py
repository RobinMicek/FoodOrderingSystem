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

import threading

# IMPORTS FROM PACKAGES
from flask import Flask, Blueprint, request, current_app
from flask_cors import CORS


# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from web.render_extended_template import render_extended_template
from database.handle_database import Database

# IMPORT CONSTANT VARIABLES (/app/variables.py)
from variables import FLASK_SECRET_KEY


# INICIALIZE FLASK
def create_app():
    app = Flask(
        __name__,
        static_folder="files")
    app.secret_key = FLASK_SECRET_KEY
    app.debug = False
    CORS(app)
    
    return app

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

# SocketIO
from flask_socketio import SocketIO
socketio = SocketIO(
    app, 
    cors_allowed_origins="*"
)
import blueprints.socketio



# RUN THE FLASK TEST SERVER
if __name__ == "__main__":

    socketio.run(
        app,
        host="0.0.0.0",
        debug=True,
        port=8080
    )

    # !!!!!!
    # RUN WITH COMMAND "python3 -m gunicorn -k gevent -w 1 --bind 0.0.0.0:8080 --chdir ./app/web app:app"
    #
    # Otherwise change from app import socketio -> from __main__ import socketion - in ./blueprints/socketio.py
    # In that case RabbitMQ thread will not work since the default socketio/flask dev server cannot handle separate thread
    # !!!!!!