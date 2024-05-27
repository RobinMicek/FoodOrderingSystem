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
from flask import Flask, Blueprint, render_template, request, redirect, jsonify

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from classes.auth_wrappers import auth_require_admin
from classes.accounts import Account
from classes.orders import Order
from classes.rabbitmq import RabbitMQ

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

@b_accounts.route("/view")
@auth_require_admin
def page_accounts_view():
    id = request.args.get("id", None)
    
    account = Account().user_info_from_id(accountId=id)
    orders = Order().all_account_orders(accountId=id)
    wallet_refills = Account().get_all_account_refills(accountId=id)

    return render_extended_template("accounts_view.html",
        account_info=account,
        orders=orders,
        wallet_refills=wallet_refills)


@b_accounts.route("/toggle-active")
@auth_require_admin
def page_accounts_toggleActive():

    id = request.args.get("id", None)
    Account().update_active(accountId=id)

    return redirect("/accounts")


@b_accounts.route("/refill-wallet")
@auth_require_admin
def page_accounts_refillWallet():

    accountId = request.args.get("accountId", None)
    amount = request.args.get("amount", None)
    Account().refill_wallet(accountId=accountId, amount=amount, establishmentId=0)

    return redirect(f"/accounts/view?id={ accountId }")
