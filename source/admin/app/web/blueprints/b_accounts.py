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
from flask import Flask, Blueprint, render_template, request, redirect, jsonify

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.auth_wrappers import auth_require_admin
from classes.accounts import Account

from web.render_extended_template import render_extended_template

# IMPORT CONSTANT VARIABLES (/app/variables.py)


# INICIALIZE BLUEPRINT
b_accounts = Blueprint(
    "accounts", 
    __name__,
    template_folder='templates'
)

# ROUTES
@b_accounts.route("/")
@auth_require_admin
def page_accounts():

    return render_extended_template("accounts_list.html",
        accounts=Account().all_accounts())


@b_accounts.route("/toggle-active")
@auth_require_admin
def page_accounts_toggleActive():

    id = request.args.get("id", None)
    Account().update_active(accountId=id)

    return redirect("/accounts")
