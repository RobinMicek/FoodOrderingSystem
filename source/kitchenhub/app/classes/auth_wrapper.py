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
from flask import session, redirect, jsonify, request


# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

# IMPORT CONSTANT VARIABLES (/app/variables.py)


# These wrappers  are used to check if current user has required level to access requested content.

def auth_require_login(func):
    def wrap(*args, **kwargs):
        if session.get("auth", None) == True:
            return func(*args, **kwargs)

        else:
            return redirect("/login")
    
    wrap.__name__ = func.__name__
    return wrap