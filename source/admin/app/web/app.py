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
import re

# IMPORTS FROM PACKAGES
from flask import Flask, Blueprint, request
from flask_cors import CORS
from werkzeug.datastructures import MultiDict

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from web.render_extended_template import render_extended_template


# IMPORT CONSTANT VARIABLES (/app/variables.py)
from variables import FLASK_SECRET_KEY


# INICIALIZE FLASK
app = Flask(
    __name__,
    static_folder="files",
    )
app.secret_key = FLASK_SECRET_KEY
CORS(app)


# Remove banned characters on form data
def remove_characters_from_form_data():
    pattern = r"[`'\"\\]"

    form_data = request.form.to_dict(flat=False)
    modified_data = MultiDict()

    for key in form_data:
        if isinstance(form_data[key], list):
            modified_data.setlist(key, [re.sub(pattern, '', item) for item in form_data[key]])
        else:
            modified_data[key] = re.sub(pattern, '', form_data[key])

    request.form = modified_data

app.before_request(remove_characters_from_form_data)


# IMPORT BLUEPRINTS
from blueprints.b_homepage import b_homepage
app.register_blueprint(b_homepage)

from blueprints.b_establishments import b_establishments
app.register_blueprint(b_establishments, url_prefix="/establishments")

from blueprints.b_products import b_products
app.register_blueprint(b_products, url_prefix="/products")

from blueprints.b_menus import b_menus
app.register_blueprint(b_menus,url_prefix="/menus")

from blueprints.b_orders import b_orders
app.register_blueprint(b_orders,url_prefix="/orders")

from blueprints.b_accounts import b_accounts
app.register_blueprint(b_accounts,url_prefix="/accounts")

from blueprints.b_texts import b_texts
app.register_blueprint(b_texts)


# Auth admin
from blueprints.b_auth import b_auth
app.register_blueprint(b_auth)


# 404 ERROR HANDLING
def handle_bad_request(e):
    return render_extended_template("base.html")
app.register_error_handler(404, handle_bad_request)


# API
from blueprints.b_api import b_api
app.register_blueprint(b_api, url_prefix="/api")

# Establishment API
from blueprints.b_kitchenhub import b_kitchenhub
app.register_blueprint(b_kitchenhub, url_prefix="/kitchenhub")


# SocketIO
from flask_socketio import SocketIO
socketio = SocketIO(
    app, 
    cors_allowed_origins="*"
)
import blueprints.b_socketio


# IMPORT ERROR HANDLERS
# from blueprints.b_errors import page_not_found
# app.register_error_handler(404, page_not_found)


# RUN THE FLASK TEST SERVER
while __name__ == "__main__":

    socketio.run(
        app,
        host="0.0.0.0",
        debug=True,
        port=8000
    )
