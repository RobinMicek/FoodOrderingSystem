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


# INICIALIZE BLUEPRINT
b_screens = Blueprint(
    "screens", 
    __name__,
    template_folder='templates'
)


# ROUTES
@b_screens.route("/call-screen")
@auth_require_login
def page_callScreen():
    return render_extended_template("/screens/call-screen.html")


@b_screens.route("/kitchen-screen")
@auth_require_login
def page_kitchenScreen():
    return render_extended_template("/screens/kitchen-screen.html")


@b_screens.route("/collect-point")
@auth_require_login
def page_collectPoint():
    return render_extended_template("/screens/collect-point.html")


@b_screens.route("/kitchen-collect")
@auth_require_login
def page_kitchenCollect():
    return render_extended_template("/screens/kitchen-collect.html")