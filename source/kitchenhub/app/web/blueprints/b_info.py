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

from classes.auth_wrapper import auth_require_login
from web.render_extended_template import render_extended_template

from classes.info import Info

# IMPORT CONSTANT VARIABLES (/app/variables.py)


# INICIALIZE BLUEPRINT
b_info = Blueprint(
    "info", 
    __name__,
    template_folder='templates'
)


# ROUTES
@b_info.route("/info")
@auth_require_login
def page_stats():
    return render_extended_template("info.html",
        orders = Info().orders()
    )