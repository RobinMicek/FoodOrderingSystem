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

# IMPORTS FROM PACKAGES
from flask import Flask, Blueprint, render_template, request, redirect, jsonify, session

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.auth_wrapper import auth_require_login
from web.render_extended_template import render_extended_template
from classes.orders import Order

# IMPORT CONSTANT VARIABLES (/app/variables.py)


# INICIALIZE BLUEPRINT
b_funcs = Blueprint(
    "b_funcs", 
    __name__,
    template_folder='templates'
)


# ROUTES
@b_funcs.route("/socket-client-connect")
@auth_require_login
def func_socketClientConnect():
    from blueprints.socketio import socketioClient_connect
    socketioClient_connect()

    return redirect(request.referrer)


@b_funcs.route("/get-orders")
@auth_require_login
def func_getOrders():
    Order().store_orders_from_api()

    return redirect(request.referrer)


@b_funcs.route("/sync-orders")
@auth_require_login
def func_syncOrders():
    Order().sync_local_orders()

    return redirect(request.referrer)


@b_funcs.route("/send-local-socket")
def func_sendLocalSocket():
    Order().send_orders_local_socket()

    if request.referrer:
        return redirect(request.referrer)
    else:
        return "0"


@b_funcs.route("/toggle-status")
@auth_require_login
def func_toggleStatus():
    try:
        Order().toggle_local_status(orderId=request.args.get("orderId", "None"))
        return "True"
    
    except Exception:
        return "False" 
