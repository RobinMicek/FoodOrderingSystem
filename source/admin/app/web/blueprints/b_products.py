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
from classes.products import Product

from web.render_extended_template import render_extended_template

# IMPORT CONSTANT VARIABLES (/app/variables.py)


# INICIALIZE BLUEPRINT
b_products = Blueprint(
    "products", 
    __name__,
    template_folder='templates'
)

# ROUTES
@b_products.route("/")
@auth_require_admin
def page_products():

    return render_extended_template("products_list.html",
        products=Product().all_products())


@b_products.route("/new", methods=["POST", "GET"])
@auth_require_admin
def page_products_new():

    if request.method != "POST":
        return render_extended_template("products_new.html")
        
    else:
        data = request.form.to_dict()
        
        if "image" in request.files and request.files.get('image').filename:     
            data["image"] = request.files["image"]
        else:
            data["image"] = None

        id = Product().create_new_product(data=data)

        return redirect(f"/products/edit?id={id}")


@b_products.route("/edit", methods=["POST", "GET"])
@auth_require_admin
def page_products_edit():

    id = request.args.get("id", None)
    if request.method != "POST":
        if id != None:
            return render_extended_template("products_edit.html",
                prod_info = Product().info(productId=id),
                stats = {
                    "purchases": {
                        "today": Product().number_of_purchases(productId = id, timeWindow = "today"),
                        "month": Product().number_of_purchases(productId = id, timeWindow = "month"),
                        "year": Product().number_of_purchases(productId = id, timeWindow = "year"),
                        "allTime": Product().number_of_purchases(productId = id, timeWindow = "allTime")                        
                    },
                    "revenue": {
                        "today": Product().revenue(productId = id, timeWindow = "today"),
                        "month": Product().revenue(productId = id, timeWindow = "month"),
                        "year": Product().revenue(productId = id, timeWindow = "year"),
                        "allTime": Product().revenue(productId = id, timeWindow = "allTime")
                    }
                })        
        else:
            return redirect("/products")        
    else:
        data = request.form.to_dict()

        if "image" in request.files and request.files.get('image').filename:     
            data["image"] = request.files["image"]
        else:
            data["image"] = None

        Product().update_product(data=data)

        return redirect(f"/products/edit?id={data['productId']}")
    
@b_products.route("/toggle-show")
@auth_require_admin
def page_products_toggleShow():

    id = request.args.get("id", None)
    Product().update_show(productId=id)

    return redirect("/products")
