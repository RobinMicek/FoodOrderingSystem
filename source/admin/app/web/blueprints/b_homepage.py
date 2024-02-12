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
from flask import Flask, Blueprint, render_template, request, redirect

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.auth_wrappers import auth_require_admin

from classes.stats import Stats

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

    timeWindow = request.args.get("timeWindow", None)
    timeWindow = timeWindow if timeWindow in ["today", "week", "month", "year"] else "today"

    return render_extended_template("dashboard.html",
        stats = {
            "stats": Stats().stats(),
            "most_purchased_products": Stats().most_purchased_products(timeWindow=timeWindow),
            "most_visited_establishments": Stats().most_visited_establishments(timeWindow=timeWindow),
            "revenue_per_day": Stats().revenue_per_day(),
            "revenue_per_hour": Stats().revenue_per_hour(),
            "revenue_per_establishment": Stats().revenue_per_establishment(timeWindow=timeWindow)
        }
    )