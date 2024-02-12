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
from classes.menus import Menu
from classes.products import Product

from web.render_extended_template import render_extended_template

# IMPORT CONSTANT VARIABLES (/app/variables.py)


# INICIALIZE BLUEPRINT
b_menus = Blueprint(
    "menus", 
    __name__,
    template_folder='templates'
)

# ROUTES
@b_menus.route("/")
@auth_require_admin
def page_products():

    return render_extended_template("menus_list.html",
        menus=Menu().all_menus())


@b_menus.route("/new", methods=["POST", "GET"])
@auth_require_admin
def page_products_new():

    if request.method != "POST":
        return render_extended_template("menus_new.html")
        
    else:
        data = request.form.to_dict()
        
        if "image" in request.files and request.files.get('image').filename:     
            data["image"] = request.files["image"]
        else:
            data["image"] = None

        id = Menu().create_new_menu(data=data)

        return redirect(f"/menus/edit?id={id}")


@b_menus.route("/edit", methods=["POST", "GET"])
@auth_require_admin
def page_products_edit():

    id = request.args.get("id", None)
    if request.method != "POST":
        if id != None:
            return render_extended_template("menus_edit.html",
                menu = Menu().info(menuId=id))        
        else:
            return redirect("/menus")        
    else:
        data = request.form.to_dict()

        if "image" in request.files and request.files.get('image').filename:     
            data["image"] = request.files["image"]
        else:
            data["image"] = None

        Menu().update_menu(data=data)

        return redirect(f"/menus/edit?id={data['menuId']}")
    

@b_menus.route("/edit-products", methods=["POST", "GET"])
@auth_require_admin
def page_products_editProducts():

    id = request.args.get("id", None)
    if request.method != "POST":
        if id != None:
            return render_extended_template("menus_products_edit.html",
                menu = Menu().all_info(menuId=id),
                products = Product().all_products())
        else:
            return redirect("/menus")        
    else:
        data = request.form.to_dict()
        data["products"] = request.form.getlist("products")

        Menu().update_products(data=data)

        return redirect(f"/menus/edit-products?id={data['menuId']}")

    
@b_menus.route("/toggle-show")
@auth_require_admin
def page_products_toggleShow():

    id = request.args.get("id", None)
    Menu().update_show(menuId=id)

    return redirect("/menus")
