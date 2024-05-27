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
import datetime

# IMPORTS FROM PACKAGES
from flask import Flask, Blueprint, render_template, request, redirect

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.auth_wrappers import auth_require_admin

from classes.stats import Stats
from classes.establishments import Establishment

from web.render_extended_template import render_extended_template

# IMPORT CONSTANT VARIABLES (/app/variables.py)


# INICIALIZE BLUEPRINT
b_homepage = Blueprint(
    "homepage", 
    __name__,
    template_folder='templates'
)

# ROUTES
@b_homepage.route("/")
@auth_require_admin
def page_homepage():
    rangeFrom = request.args.get("rangeFrom", datetime.date.today())
    rangeTo = request.args.get("rangeTo", datetime.date.today())
    establishmentId = request.args.get("selectedEstablishment", "None")

    return render_extended_template(f"dashboard.html",
        stats_sum = Stats().stats_sum(rangeTo=rangeTo, rangeFrom=rangeFrom),
        stats = Stats().stats(rangeTo=rangeTo, rangeFrom=rangeFrom),
        all_establishments = Establishment().all_establishments(),
        establishment_sum = Stats().establishment_sum(rangeTo=rangeTo, rangeFrom=rangeFrom, establishmentId=establishmentId)
    )