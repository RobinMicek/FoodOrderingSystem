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
from flask import render_template, session

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)


# IMPORT CONSTANT VARIABLES (/app/variables.py)
from variables import CONFIG


# This function wraps the render_template function from flask
# and inputs some basic variables that are present on each page.
def render_extended_template(*args, **kwargs):

    return render_template(
        *args, **kwargs,
        account = session["account"],
        company_name = CONFIG["companyInfo"]["companyName"]
    )