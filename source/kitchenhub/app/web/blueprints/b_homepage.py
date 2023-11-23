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

# IMPORT CONSTANT VARIABLES (/app/variables.py)
from getConfig import getConfig


# INICIALIZE BLUEPRINT
b_homepage = Blueprint(
    "homepage", 
    __name__,
    template_folder='templates'
)


# ROUTES
@b_homepage.route("/")
def page_home():
    if getConfig() != None:
        if session.get("auth", None) == True:
            return render_extended_template("home.html")    
        else:
            return redirect("/login")
    else:
        return redirect("/first-time-setup")    