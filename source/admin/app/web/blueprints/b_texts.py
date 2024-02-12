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
import json

# IMPORTS FROM PACKAGES
from flask import Flask, Blueprint, render_template, request, redirect
from pprint import pprint

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.auth_wrappers import auth_require_admin

from web.render_extended_template import render_extended_template

# IMPORT CONSTANT VARIABLES (/app/variables.py)


# INICIALIZE BLUEPRINT
b_texts = Blueprint(
    "texts", 
    __name__,
    template_folder='templates'
)

# ROUTES

# Configuration
@b_texts.route("/configure", methods=["POST", "GET"])
@auth_require_admin
def page_configuration():

    if request.method != "POST":
        
        oldConfigurationJSON = {}
        with open(f"{root_folder}/files/storage/texts/config.json", "r") as file:
            oldConfigurationJSON = json.load(file)

        return render_extended_template("configuration.html",
            oldConfigurationJSON = oldConfigurationJSON)
        
    else:        
        configurationJSON = (request.data).decode("utf-8")

        if configurationJSON != None:
            with open(f"{root_folder}/files/storage/texts/config.json", "w+") as file:
                file.write(configurationJSON)
        
        return redirect(f"/configure")


# Terms
@b_texts.route("/terms", methods=["POST", "GET"])
@auth_require_admin
def page_terms():

    if request.method != "POST":

        oldTerms = ""
        with open(f"{root_folder}/files/storage/texts/terms-of-service.txt", "r+") as file:
                oldTerms = file.read()

        return render_extended_template("terms.html",
            oldTerms = oldTerms)
        
    else:        
        newTerms = request.form.get("terms", None)

        if newTerms != None:
            with open(f"{root_folder}/files/storage/texts/terms-of-service.txt", "w+") as file:
                file.write(newTerms)

        return redirect(f"/terms")
