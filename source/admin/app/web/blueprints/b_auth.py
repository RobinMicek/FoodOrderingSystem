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
from flask import Flask, Blueprint, render_template, request, redirect, jsonify, session

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.accounts import Account
from classes.auth_wrappers import auth_require_token

# IMPORT CONSTANT VARIABLES (/app/variables.py)


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
        account = Account()

        email = request.form.get("email", "None")
        password = request.form.get("password", "None")

        if account.auth_password(email=email, password=password) == True:
            session["account"] = f"{email}"
            session["role"] = account.user_info_from_email(email=f"{email}")["role"]
            session["active"] = account.user_info_from_email(email=f"{email}")["active"]

            return redirect("/")
        else:
            return render_template("login.html"), 401
        

@b_auth.route("/logout")
def page_logout():

    session.pop("account", None)
    session.pop("role", None)
    session.pop("active", None)

    return redirect("/")