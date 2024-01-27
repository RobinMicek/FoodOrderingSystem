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

from classes.auth_wrappers import auth_require_token

# IMPORT CONSTANT VARIABLES (/app/variables.py)


# INICIALIZE BLUEPRINT
b_api = Blueprint(
    "b_api", 
    __name__,
    template_folder='templates'
)

# ROUTES

# AUTH
@b_api.route("/login", methods=["POST"])
def api_login():

    email = request.json.get("email", "None")
    password = request.json.get("password", "None")

    if Account().auth_password(email=email, password=password) == True and Account().user_info(email=email)["active"] == 1:

        # Update account token
        new_token = Account().update_token(email=email)

        if new_token != False:

            return jsonify({
                    "token": Account().user_info(email=email)["token"]                    
                }), 200
        
        else:
            return jsonify({
                "message": "Something went wrong with the login!"
            }), 500

    return jsonify({
            "message": "Login denied!"
        }), 401
    

@b_api.route("/register", methods=["POST"])
def api_register():

    data = request.json
    data["role"] = "user"

    new_account = Account().create_new_account(**data)

    return jsonify({
            "status": new_account
        }), 200 if new_account == True else 400



# ESTABLISHMENTS
@b_api.route("/get-all-establishments", methods=["GET"])
@auth_require_token
def api_getAllEstablishments():

    data = []
    for establishment in Establishment().all_establishments():
        establishment_data = Establishment().all_info(establishmentId=establishment["establishmentId"])
        del establishment_data["menus"]
        del establishment_data["openingHours"]

        data += [establishment_data] if establishment_data["show"] == 1 else [] 

    return jsonify({
            "data": data
        }), 200 


@b_api.route("/get-establishment", methods=["GET"])
@auth_require_token
def api_getEstablishment():

    establishmentId = request.args.get("establishmentId", "None")

    if establishmentId.isdigit() == True:
        establishment_data = Establishment().all_info(establishmentId=establishmentId)
        if establishment_data != False:
            del establishment_data["openingHours"]

            establishment_data["menus"] = [menu for menu in establishment_data["menus"] if menu["show"] != 0]

            return jsonify({
                    "data": establishment_data
                }), 200 
    
    return jsonify({
                "message": "Could not find the establishment!"
            }), 404



# Menus
@b_api.route("/get-menu", methods=["GET"])
@auth_require_token
def api_getMenu():

    menuId = request.args.get("menuId", "None")

    if menuId.isdigit() == True:
        menu_data = Menu().all_info(menuId=menuId)
        if menu_data != False and menu_data["show"] == 1:

            return jsonify({
                    "data": menu_data
                }), 200 
    
    return jsonify({
                "message": "Could not find the menu!"
            }), 404


# ORDERS
@b_api.route("/create-order", methods=["POST"])
@auth_require_token
def api_createOrder():

    data = request.json
    data["accountId"] = Account().user_info_from_token(token=request.headers.get("Authorization", "None")).get("accountId", "Nonew")

    new_order = Order().create_order(data=data)
    if new_order != False:
        return jsonify({
            "data": new_order
        }), 200 

    return jsonify({
                "message": "Could not create new order!"
            }), 400


@b_api.route("/get-order", methods=["get"])
@auth_require_token
def api_getOrder():

    orderId = request.args.get("orderId", "None")
    order = Order().info(orderId=orderId)
    user = Account().user_info_from_token(token=request.headers.get("Authorization", "None"))["accountId"]

    if order != [] and order["accountId"] == user:
        order["products"] = Order().products(orderId=orderId)

        return jsonify({
            "data": order
        }), 200 

    return jsonify({
                "message": "Could not find the order!"
            }), 400


@b_api.route("/get-all-orders", methods=["get"])
@auth_require_token
def api_getAllOrder():

    return jsonify({
        "data": Order().all_account_orders(accountId=Account().user_info_from_token(token=request.headers.get("Authorization", "None"))["accountId"])
    }), 200 