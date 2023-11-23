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

from database.handle_database import Database
from classes.server_requests import ServerRequests

# IMPORT CONSTANT VARIABLES (/app/variables.py)
from getConfig import getConfig

# INICIALIZE BLUEPRINT
b_fts = Blueprint(
    "firstTimeSetup", 
    __name__,
    template_folder='templates'
)


# ROUTES
@b_fts.route("/first-time-setup", methods=["POST", "GET"])
def page_fts():

    if getConfig() != None:
        return redirect("/")

    else: 
        if request.method != "POST":
            return render_template("fts.html")
        
        else:
            # Replace HTTPS with HTTP - I have tried so hard to make it work over HTTPS,
            # but i have always run into a "Maximum Recursion" error.
            # It appears to be a bug within flask.
            serverUrl = request.form["serverUrl"]
            if "https://" in serverUrl:
                serverUrl = serverUrl.replace("https://", "http://")

            establishmentName = ServerRequests().get_establishment_fts(serverUrl=serverUrl, establishmentSlug=request.form["establishmentSlug"], establishmentToken=request.form["establishmentToken"])

            if establishmentName == False:
                return redirect("/first-time-setup")

            else:
                establishmentName = establishmentName["name"] 
                    
                db = Database()
                db.cursor.execute(f"""
                    INSERT INTO app_configuration
                    (serverUrl, establishmentSlug, establishmentToken, pin, establishmentName)
                                
                    VALUES
                    ('{serverUrl}', '{request.form["establishmentSlug"]}', '{request.form["establishmentToken"]}', '{request.form["pin"]}', '{establishmentName}')
                """)
                db.close()

                return redirect("/")



