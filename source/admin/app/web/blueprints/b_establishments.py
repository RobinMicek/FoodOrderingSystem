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
from classes.establishments import Establishment
from classes.menus import Menu

from web.render_extended_template import render_extended_template

# IMPORT CONSTANT VARIABLES (/app/variables.py)


# INICIALIZE BLUEPRINT
b_establishments = Blueprint(
    "establishments", 
    __name__,
    template_folder='templates'
)

# ROUTES
@b_establishments.route("/")
@auth_require_admin
def page_establishments():


    return render_extended_template("establishments_list.html",
        establishments=Establishment().all_establishments())


@b_establishments.route("/new", methods=["POST", "GET"])
@auth_require_admin
def page_establishments_new():

    if request.method != "POST":
        return render_extended_template("establishments_new.html",
            all_menus = Menu().all_menus())
        
    else:
        data = request.form.to_dict()
        data["menus"] = request.form.getlist("menus")
        
        if "image" in request.files and request.files.get('image').filename:     
            data["image"] = request.files["image"]
        else:
            data["image"] = None
        
        id = Establishment().create_new_establishment(data=data)

        return redirect(f"/establishments//edit?id={id}")


@b_establishments.route("/edit", methods=["POST", "GET"])
@auth_require_admin
def page_establishments_edit():
    id = request.args.get("id", None)
    if request.method != "POST":
        if id != None:
            return render_extended_template("establishments_edit.html",
                est_info = Establishment().all_info(establishmentId=id),
                all_menus = Menu().all_menus(),
                stats = {
                    "orders": {
                        "today": Establishment().number_of_orders(establishmentId = id, timeWindow = "today"),
                        "month": Establishment().number_of_orders(establishmentId = id, timeWindow = "month"),
                        "year": Establishment().number_of_orders(establishmentId = id, timeWindow = "year"),
                        "allTime": Establishment().number_of_orders(establishmentId = id, timeWindow = "allTime"),
                        "orders_per_day": Establishment().orders_per_day(establishmentId = id)
                    },
                    "revenue": {
                        "today": Establishment().revenue(establishmentId = id, timeWindow = "today"),
                        "month": Establishment().revenue(establishmentId = id, timeWindow = "month"),
                        "year": Establishment().revenue(establishmentId = id, timeWindow = "year"),
                        "allTime": Establishment().revenue(establishmentId = id, timeWindow = "allTime"),
                        "revenue_per_day": Establishment().revenue_per_day(establishmentId = id)
                    }
                })
        else:
            return redirect("/establishments")        
    else:
        data = request.form.to_dict()
        data["menus"] = request.form.getlist("menus")   

        if "image" in request.files and request.files.get('image').filename:     
            data["image"] = request.files["image"]
        else:
            data["image"] = None
        
        Establishment().update_establishment(data=data)

        return redirect(f"/establishments/edit?id={data['establishmentId']}")


@b_establishments.route("/toggle-show")
@auth_require_admin
def page_establishments_toggleShow():
    
    id = request.args.get("id", None)
    Establishment().update_show(establishmentId=id)

    return redirect("/establishments")