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

import json

# IMPORTS FROM PACKAGES

# IMPORTS FROM OTHER FILES
# Fix
root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from random_string import random_string


# CONFIG FILE
CONFIG = ""
with open(f"{root_folder}/app/web/files/storage/texts/config.json", "r") as file:
    CONFIG = json.load(file)


# HASHING
HASH_SALT = str(os.environ.get("KO_HASH_SALT", None))


# FLASK
FLASK_SECRET_KEY = random_string(length=32)


# DATABASE SERVER INFO
DB_HOST = str(os.environ.get("KO_DB_HOST", None))
DB_NAME = str(os.environ.get("KO_DB_NAME", None)) 
DB_USER = str(os.environ.get("KO_DB_USER", None))
DB_PASSWORD = str(os.environ.get("KO_DB_PASSWORD", None))
DB_SSL_CA = str(os.environ.get("KO_DB_SSL_CA", None)) # If not using SSL -> Leave blank