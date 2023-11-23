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
from flask import Flask, Blueprint, render_template, request, redirect, jsonify

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.accounts import Account
from classes.establishments import Establishment
from classes.menus import Menu
from classes.orders import Order

from classes.auth_wrappers import auth_require_establishment

# IMPORT CONSTANT VARIABLES (/app/variables.py)


# INICIALIZE BLUEPRINT
b_kitchenhub = Blueprint(
    "kitchenhub", 
    __name__,
    template_folder='templates'
)

# ROUTES

# ESTABLISHMENTS
@b_kitchenhub.route("/get-all-establishments", methods=["GET"])
@auth_require_establishment
def kitchenhub_api_getAllEstablishments(establishmentId):

    data = []
    for establishment in Establishment().all_establishments():
        establishment_data = Establishment().all_info(establishmentId=establishment["establishmentId"])
        del establishment_data["menus"]
        del establishment_data["openingHours"]

        data += [establishment_data]

    return jsonify({
            "data": data
        }), 200 


@b_kitchenhub.route("/get-establishment", methods=["GET"])
@auth_require_establishment
def kitchenhub_api_getEstablishment(establishmentId):

    
    establishment_data = Establishment().info(establishmentId=establishmentId)
    if establishment_data != False:
        del establishment_data["slug"]
        del establishment_data["token"]

        return jsonify({
                "data": establishment_data
            }), 200 
    
    else:
        return jsonify({
                "message": "Could not find the establishment!"
            }), 404


# ORDERS
@b_kitchenhub.route("/get-all-orders", methods=["get"])
@auth_require_establishment
def kitchenhub_api_getAllOrders(establishmentId):

    all_orders = Order().all_establishment_orders_kitchenhub(establishmentId=establishmentId)
    
    return jsonify({
        "data": all_orders
    }), 200


@b_kitchenhub.route("/update-order-status", methods=["POST"])
@auth_require_establishment
def kitchenhub_api_updateOrderStatus(establishmentId):

    try:
        Order().update_status(orderId=request.json.get("orderId", None), newStatus=request.json.get("newStatus", None))
    
        return jsonify({
            "status": True
        }), 200
    
    except:
        return jsonify({
            "status": False
        }), 500