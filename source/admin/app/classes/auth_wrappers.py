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
from flask import session, redirect, jsonify, request


# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from database.handle_database import Database
from logs import create_log
from random_string import random_string
from classes.accounts import Account
from classes.establishments import Establishment

# IMPORT CONSTANT VARIABLES (/app/variables.py)


# These wrappers  are used to check if current user has required level to access requested content.


# ADMIN PANEL
def auth_require_admin(func):
    def wrap(*args, **kwargs):
        if session.get("account", None) != None and session.get("role", None) == "admin" and session.get("active", 0) == 1:
            return func(*args, **kwargs)

        else:
            return redirect("/login")
    
    wrap.__name__ = func.__name__
    return wrap
        

# API
def auth_require_token(func):
    def wrap(*args, **kwargs):
        account = Account()

        if str(request.headers.get("Authorization", "None"))[:6] == "Bearer":
            if account.auth_token(token=request.headers.get("Authorization", "None")) != False:
                return func(*args, **kwargs)
        
        return jsonify({
            "status": 401,
            "message": "Valid user token required!"
        }), 401

    wrap.__name__ = func.__name__
    return wrap


def auth_require_pos(func):
    def wrap(*args, **kwargs):
        account = Account()

        if str(request.headers.get("Authorization", "None"))[:6] == "Bearer":
            if account.user_info_from_token(token=request.headers.get("Authorization", "None"))["role"] == "pos":
                return func(*args, **kwargs)
        
        return jsonify({
            "status": 401,
            "message": "Valid user token required!"
        }), 401

    wrap.__name__ = func.__name__
    return wrap


# ESTABLISHMENT API
def auth_require_establishment(func):
    def wrap(*args, **kwargs):
        establishment = Establishment()
        establishmentId = establishment.auth(slug=request.headers.get("EstablishmentSlug", "None"), token=request.headers.get("EstablishmentToken", "None"))
        
        if  establishmentId != False:
            return func(establishmentId, *args, **kwargs)
    
        return jsonify({
            "status": 401,
            "message": "Valid establishment credentials required!"
        }), 401

    wrap.__name__ = func.__name__
    return wrap