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

# IMPORT CONSTANT VARIABLES (/app/variables.py)
from getConfig import getConfig


# INICIALIZE BLUEPRINT
b_auth = Blueprint(
    "auth", 
    __name__,
    template_folder='templates'
)


# ROUTES
@b_auth.route("/login", methods=["POST", "GET"])
def page_login():

    if request.method != "POST":
        return render_template("login.html")
    
    else:
        pin = request.form.get("pin", "None")
        CONFIG = getConfig()

        if str(pin) == str(CONFIG["pin"]): 
            session["auth"] = True

            return redirect("/")
        else:
            return render_template("login.html"), 401
        

@b_auth.route("/logout")
def page_logout():

    session.pop("auth", None)

    return redirect("/")