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

# IMPORTS FROM PACKAGES
from flask import Flask, Blueprint, render_template, request, redirect, jsonify

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.auth_wrappers import auth_require_admin
from classes.orders import Order

from web.render_extended_template import render_extended_template

# IMPORT CONSTANT VARIABLES (/app/variables.py)


# INICIALIZE BLUEPRINT
b_orders = Blueprint(
    "orders", 
    __name__,
    template_folder='templates'
)

# ROUTES
@b_orders.route("/")
@auth_require_admin
def page_orders():

    return render_extended_template("orders_list.html",
        orders=Order().all_orders())


@b_orders.route("/view")
@auth_require_admin
def page_orders_view():

    id = request.args.get("id", None)
    order = Order().info(orderId=id)
    order["products"] = Order().products(orderId=id)

    return render_extended_template("orders_view.html",
        order=order)


@b_orders.route("/cancel-order")
@auth_require_admin
def page_orders_cancel():

    id = request.args.get("id", None)
    Order().cancel_order(orderId=id)
    
    return redirect(f"/orders/view?id={id}")